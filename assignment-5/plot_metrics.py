from utils import *
from metrics import *

import pandas as pd
import matplotlib.pyplot as plt
plt.tight_layout()

if __name__ == "__main__":
    import sys
    try: path_original, path_prefix_compressed = sys.argv[1], sys.argv[2]
    except: print("usage: metrics.py path_original path_prefix_compressed")
    
    root, prefix, _ = split_root_name_ext(path_prefix_compressed)
    path_compressed_list = [os.path.join(root, fname) for fname in os.listdir(root if len(root) > 0 else ".") 
                            if (fname.startswith(prefix) and fname.endswith(DEFAULT_EXT))]
    print(f"Original: {path_original}")
    # print(f"Compressed: {", ".join(path_compressed_list)}")

    rmse_list = [rmse(load(path_original), load(path_compressed))
                 for path_compressed in path_compressed_list]
    rho_list = [compression_ratio(path_original, path_compressed)[0]
                for path_compressed in path_compressed_list]
    k_list = [int(path_compressed[path_compressed.index(prefix) + len(prefix) : -4])
              for path_compressed in path_compressed_list]
    
    df = pd.DataFrame({ "Number of components": k_list, 
                        "RMSE": rmse_list, 
                        "Compression ratio": rho_list })
    df = df.sort_values("Number of components")
    print(df.to_string(index=False))

    plt.plot("Number of components", "Compression ratio", data=df,
             marker="o", linestyle="dashed", color="orange")
    plt.title(os.path.basename(path_original))
    plt.xlabel("Number of components")
    plt.ylabel("Compression ratio")
    plt.savefig(f"metrics\\plot-{prefix[:-1]}-rho.png")
    plt.show()

    plt.plot("Number of components", "RMSE", data=df,
             marker="o", linestyle="dashed", color="blue")
    plt.title(os.path.basename(path_original))
    plt.xlabel("Number of components")
    plt.ylabel("RMSE")
    plt.savefig(f"metrics\\plot-{prefix[:-1]}-rmse.png")
    plt.show()

    normalized_df = (df - df.min()) / (df.max() - df.min())
    normalized_df["Number of components"] = df["Number of components"]
    plt.plot("Number of components", "Compression ratio", data=normalized_df,
             marker="o", linestyle="dashed", color="orange", label="Compression ratio")
    plt.plot("Number of components", "RMSE", data=normalized_df,
             marker="o", linestyle="dashed", color="blue", label="RMSE")
    plt.legend(loc="center right")
    plt.title(os.path.basename(path_original))
    plt.xlabel("Number of components")
    plt.ylabel("Normalized values to 0-1 range")
    plt.savefig(f"metrics\\plot-{prefix[:-1]}.png")
    plt.show()

