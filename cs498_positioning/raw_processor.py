from positioning import *

if __name__ == '__main__':
    with open("data/2019_12_06_00_19_15_raw_data.txt", "r") as fin:
        with open("data/2019_12_06_00_19_15_raw_rngs.csv", "w") as fout:
            keys = None
            for line in fin:
                dist = process_info(line)
                if dist is None:
                    continue

                if keys is None:
                    keys = dist.keys()
                    fout.write(",".join(keys) + "\n")

                result = []
                for key in keys:
                    if key in dist.keys():
                        result.append(dist[key])
                    else:
                        result.append(0)
                fout.write(",".join([str(x) for x in result]) + "\n")