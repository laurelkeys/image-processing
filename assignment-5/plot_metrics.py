from utils import *
from metrics import *

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()

if __name__ == "__main__":
    import sys
    try: path_original, path_prefix_compressed = sys.argv[1], sys.argv[2]
    except: print("usage: metrics.py path_original path_prefix_compressed")
    
    root, prefix, _ = split_root_name_ext(path_prefix_compressed)
    path_compressed_list = [os.path.join(root, fname) for fname in os.listdir(root) 
                            if fname.startswith(prefix)]
    print(f"Original: {path_original}")
    print(f"Compressed: {', '.join(path_compressed_list)}")

    rmse_list = [rmse(load(path_original), load(path_compressed))
                 for path_compressed in path_compressed_list]
    rho_list = [compression_ratio(path_original, path_compressed)[0]
                for path_compressed in path_compressed_list]
    k_list = [int(path_compressed[path_compressed.index(prefix) + len(prefix) : -4])
              for path_compressed in path_compressed_list]
    
    df = pd.DataFrame({'Number of components': k_list, 'RMSE': rmse_list, 'Compression ratio': rho_list})
    df = df.sort_values('Number of components')
    print(df)

    sns.pairplot(data=df)
    plt.show()