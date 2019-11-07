import os
import numpy as np

def rmse(original, compressed):
    ''' Returns the Root Mean Squared Error between `original` and `compressed` '''
    return np.sqrt(np.mean(np.square(original.astype('float') - compressed.astype('float'))))

def compression_ratio(path_original, path_compressed):
    ''' Returns a tuple (`compression_ratio`, `fsize_original`,  `fsize_compressed`), where
        `compression_ratio` = `fsize_compressed` / `fsize_original`, considering the file sizes in bytes '''
    fsize_original = os.path.getsize(path_original)
    fsize_compressed = os.path.getsize(path_compressed)
    return (fsize_compressed / fsize_original), fsize_original, fsize_compressed

###############################################################################

if __name__ == "__main__":
    import sys
    try: path_original, path_compressed = sys.argv[1], sys.argv[2]
    except: print("usage: metrics.py path_original path_compressed"); exit()
    
    compr_ratio, fsize_orig, fsize_compr = compression_ratio(path_original, path_compressed)
    print(f"{path_original} file size: {fsize_orig} bytes")
    print(f"{path_compressed} file size: {fsize_compr} bytes")
    print()

    from utils import load
    print(f"RMSE: {rmse(load(path_original), load(path_compressed)):.4f}")
    
    print(f"Compression ratio: {100 * compr_ratio:.2f}% = {fsize_compr} / {fsize_orig}")