import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from numba import jit
from tqdm.auto import tqdm
from multiprocessing import Pool, cpu_count

class pyfracd:
    def __init__(self, window_size=10, chunk_processing=True, chunksize=(512, 512)):
        self.window_size = window_size
        self.chunk_processing = chunk_processing
        self.chunksize = chunksize
        self.fd2_out = None
        self.se2_out = None
        self.r2_out = None
        self.ft2mUS = 1200/3937  # US survey foot to meter conversion factor
        self.ft2mInt = 0.3048    # International foot to meter conversion factor

    @staticmethod
    @jit(nopython=True, fastmath=True)
    def vario(z, window_size, imo):
        fac = 1.0 if imo == 1 else np.sqrt(2.0)
        x = np.arange(1, window_size + 1) * fac
        y = np.zeros(window_size)
        npa = np.zeros(window_size, dtype=np.int32)

        for i in range(window_size):
            diffs = z[:-i-1] - z[i+1:]
            y[i] = np.sum(diffs**2) / (2 * len(diffs))
            npa[i] = len(diffs)

        mask = npa > 0
        y = y[mask]
        x = x[mask]

        if len(x) < 2:
            return np.nan, np.nan, np.nan

        x = np.log(x)
        y = np.log(y)

        n = len(x)
        sumx = np.sum(x)
        sumy = np.sum(y)
        sumx2 = np.sum(x**2)
        sumxy = np.sum(x * y)

        b = (n * sumxy - sumx * sumy) / (n * sumx2 - sumx**2)
        a = (sumy - b * sumx) / n

        fd2 = 3.0 - b / 2.0
        yfit = a + b * x
        
        varb = (np.sum((y - yfit)**2) / (n - 2)) / (sumx2 - sumx**2 / n)
        se2 = np.sqrt(varb) / 2.0

        sum1 = np.sum((yfit - y)**2)
        sum2 = np.sum((y - np.mean(y))**2)
        r2 = 1.0 - sum1 / sum2

        return fd2, se2, r2
    
    def analyze(self, input_dir, variograms=True):
        self.input_dir = input_dir
        with rasterio.open(input_dir) as src:
            meta = src.meta.copy()
            Z = src.read(1)
            Zunit = src.crs.linear_units
            self.fd2_out = np.zeros((src.height, src.width), dtype=np.float32)
            self.se2_out = np.zeros((src.height, src.width), dtype=np.float32)
            self.r2_out = np.zeros((src.height, src.width), dtype=np.float32)

            # Get the cell size
            cell_size = src.transform[0]

            if any(unit in Zunit.lower() for unit in ["metre", "meter", "meters"]):
                pass
            elif any(unit in Zunit.lower() for unit in ["foot", "feet", "ft"]):
                if any(unit in Zunit.lower() for unit in ["us", "united states"]):
                    Z = Z * self.ft2mUS
                    cell_size = cell_size * self.ft2mUS
                else:
                    Z = Z * self.ft2mInt
                    cell_size = cell_size * self.ft2mInt
            else:
                raise ValueError("The unit of elevation 'z' must be in feet or meters.")

            if not self.chunk_processing:
                self._process_non_chunked(Z, src.height, src.width)
            else:
                self._process_chunked(Z, src.height, src.width)

            print(f"FD2 MIN : {np.nanmin(self.fd2_out)}")
            print(f"FD2 MAX : {np.nanmax(self.fd2_out)}")
            print(f"SE MIN : {np.nanmin(self.se2_out)}")
            print(f"SE MAX : {np.nanmax(self.se2_out)}")
            print(f"R2 MIN : {np.nanmin(self.r2_out)}")
            print(f"R2 MAX : {np.nanmax(self.r2_out)}")

        if variograms:
            self.plot_sample_variograms(Z)

        # Calculate window size in meters
        window_size_m = cell_size * self.window_size

        return Z, self.fd2_out, self.se2_out, self.r2_out, meta, window_size_m

    def _process_non_chunked(self, Z, height, width):
        for j in tqdm(range(height), desc="Analyzing rows"):
            for i in range(width):
                results = []
                # Horizontal slice
                data = Z[j, max(0, i-self.window_size):min(i+self.window_size+1, width)]
                if len(data) > self.window_size:
                    results.append(self.vario(data, self.window_size, 1))
                # Vertical slice
                data = Z[max(0, j-self.window_size):min(j+self.window_size+1, height), i]
                if len(data) > self.window_size:
                    results.append(self.vario(data, self.window_size, 1))
                # Diagonal slices
                for di, dj in [(1, 1), (1, -1)]:
                    data = []
                    for k in range(-self.window_size, self.window_size+1):
                        if 0 <= j+k*dj < height and 0 <= i+k*di < width:
                            data.append(Z[j+k*dj, i+k*di])
                    if len(data) > self.window_size:
                        results.append(self.vario(np.array(data), self.window_size, 2))
                if results:
                    fd2, se2, r2 = np.nanmean(results, axis=0)
                    self.fd2_out[j, i] = np.clip(fd2, 2.0, 3.0)
                    self.se2_out[j, i] = se2
                    self.r2_out[j, i] = r2

    def _process_chunked(self, Z, height, width):
        chunk_height, chunk_width = self.chunksize
        overlap = self.window_size // 2 + 1
        chunks = []
        for j in range(0, height, chunk_height - 2*overlap):
            for i in range(0, width, chunk_width - 2*overlap):
                chunk = Z[max(0, j-overlap):min(j+chunk_height+overlap, height),
                          max(0, i-overlap):min(i+chunk_width+overlap, width)]
                chunks.append((chunk, i, j))

        with tqdm(total=height, desc="Analyzing rows") as pbar:
            with Pool(cpu_count()) as pool:
                for fd2, se2, r2, i, j in pool.imap(self._process_chunk_parallel, chunks):
                    h, w = fd2.shape
                    non_overlap_h = max(0, h - 2*overlap)
                    non_overlap_w = max(0, w - 2*overlap)
                    self.fd2_out[j:j+non_overlap_h, i:i+non_overlap_w] = fd2[overlap:overlap+non_overlap_h, overlap:overlap+non_overlap_w]
                    self.se2_out[j:j+non_overlap_h, i:i+non_overlap_w] = se2[overlap:overlap+non_overlap_h, overlap:overlap+non_overlap_w]
                    self.r2_out[j:j+non_overlap_h, i:i+non_overlap_w] = r2[overlap:overlap+non_overlap_h, overlap:overlap+non_overlap_w]
                    pbar.update(non_overlap_h)

    def _process_chunk_parallel(self, args):
        Z, offset_i, offset_j = args
        fd2_out = np.zeros(Z.shape, dtype=np.float32)
        se2_out = np.zeros(Z.shape, dtype=np.float32)
        r2_out = np.zeros(Z.shape, dtype=np.float32)

        for j in range(Z.shape[0]):
            for i in range(Z.shape[1]):
                results = []
                
                # Horizontal slice
                data = Z[j, max(0, i-self.window_size):min(i+self.window_size+1, Z.shape[1])]
                if len(data) > self.window_size:
                    results.append(self.vario(data, self.window_size, 1))

                # Vertical slice
                data = Z[max(0, j-self.window_size):min(j+self.window_size+1, Z.shape[0]), i]
                if len(data) > self.window_size:
                    results.append(self.vario(data, self.window_size, 1))

                # Diagonal slices
                for di, dj in [(1, 1), (1, -1)]:
                    data = []
                    for k in range(-self.window_size, self.window_size+1):
                        if 0 <= j+k*dj < Z.shape[0] and 0 <= i+k*di < Z.shape[1]:
                            data.append(Z[j+k*dj, i+k*di])
                    if len(data) > self.window_size:
                        results.append(self.vario(np.array(data), self.window_size, 2))

                if results:
                    fd2, se2, r2 = np.nanmean(results, axis=0)
                    fd2_out[j, i] = np.clip(fd2, 2.0, 3.0)
                    se2_out[j, i] = se2
                    r2_out[j, i] = r2

        return fd2_out, se2_out, r2_out, offset_i, offset_j

    def plot_sample_variograms(self, Z):
        middle_row = Z.shape[0] // 2
        horizontal_slice = Z[middle_row, max(0, Z.shape[1]//2-self.window_size):min(Z.shape[1]//2+self.window_size+1, Z.shape[1])]
        self.plot_variogram(horizontal_slice, imo=1, title="Horizontal Variogram (Middle Row)")
        
        middle_col = Z.shape[1] // 2
        vertical_slice = Z[max(0, Z.shape[0]//2-self.window_size):min(Z.shape[0]//2+self.window_size+1, Z.shape[0]), middle_col]
        self.plot_variogram(vertical_slice, imo=1, title="Vertical Variogram (Middle Column)")
        
        diagonal_slice = [Z[i, i] for i in range(max(0, Z.shape[0]//2-self.window_size), min(Z.shape[0]//2+self.window_size+1, min(Z.shape)))]
        self.plot_variogram(diagonal_slice, imo=2, title="Diagonal Variogram")

    def plot_variogram(self, z, imo, title=None):
        z = np.array(z)
        fac = 1.0 if imo == 1 else np.sqrt(2.0)
        x = np.arange(1, self.window_size + 1) * fac
        y = np.zeros(self.window_size)
        npa = np.zeros(self.window_size, dtype=np.int32)

        for i in range(self.window_size):
            diffs = z[:-i-1] - z[i+1:]
            y[i] = np.sum(diffs**2) / (2 * len(diffs))
            npa[i] = len(diffs)

        mask = npa > 0
        y = y[mask]
        x = x[mask]

        if len(x) < 2:
            print("Not enough data points for variogram plot")
            return

        plt.figure(figsize=(5, 3))
        plt.scatter(np.log(x), np.log(y), color='blue', label='Data')
        
        coef = np.polyfit(np.log(x), np.log(y), 1)
        poly1d_fn = np.poly1d(coef)
        plt.plot(np.log(x), poly1d_fn(np.log(x)), '--r', label='Fitted Line')

        plt.xlabel('Log(Lag Distance)')
        plt.ylabel('Log(Semivariance)')
        plt.title(title or 'Variogram Plot')
        plt.legend()
        plt.grid(True)
        plt.show()

        slope = coef[0]
        fd2 = 3.0 - slope / 2.0
        print(f"Estimated Fractal Dimension: {fd2}")

    def export_results(self, fd2_output_dir, se2_output_dir, r2_output_dir, meta):
        if meta is None:
            raise ValueError("Metadata is missing. Cannot export the result.")
        
        meta.update(dtype=rasterio.float32, count=1, compress='deflate', bigtiff='IF_SAFER')

        with rasterio.open(fd2_output_dir, 'w', **meta) as dst:
            dst.write(self.fd2_out.astype(rasterio.float32), 1)
        print(f"Processed result saved to {os.path.basename(fd2_output_dir)}")

        with rasterio.open(se2_output_dir, 'w', **meta) as dst:
            dst.write(self.se2_out.astype(rasterio.float32), 1)
        print(f"Processed result saved to {os.path.basename(se2_output_dir)}")

        with rasterio.open(r2_output_dir, 'w', **meta) as dst:
            dst.write(self.r2_out.astype(rasterio.float32), 1)
        print(f"Processed result saved to {os.path.basename(r2_output_dir)}")