import collections
import argparse
import sys

def generate_itol_file(input_path, output_path):
    # 1. 色盲友好调色盘 (Okabe-Ito Palette)
    # 选用了对比度高且对红绿色盲友好的颜色
    cb_palette = [
        "#E69F00", # 橙色
        "#56B4E9", # 天蓝色
        "#009E73", # 翠绿色
        "#F0E442", # 黄色
        "#0072B2", # 蓝色
        "#D55E00", # 朱红色
        "#CC79A7", #  reddish purple
        "#000000"  # 黑色
    ]
    
    # iTOL 支持的各种形状：矩形、椭圆、菱形、三角形、五角星、垂直矩形
    shapes = ["RE", "EL", "DI", "TR", "HH", "HV"]
    
    protein_dict = collections.defaultdict(list)
    unique_domains = set()

    # 读取输入文件
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('\t')
                if len(parts) < 4:
                    continue
                
                gene_id, start, end, domain = parts[0], parts[1], parts[2], parts[3]
                protein_dict[gene_id].append({
                    'start': start,
                    'end': end,
                    'label': domain
                })
                unique_domains.add(domain)
    except FileNotFoundError:
        print(f"错误：找不到输入文件 '{input_path}'")
        sys.exit(1)

    # 自动分配颜色和形状
    sorted_domains = sorted(list(unique_domains))
    domain_to_color = {d: cb_palette[i % len(cb_palette)] for i, d in enumerate(sorted_domains)}
    domain_to_shape = {d: shapes[i % len(shapes)] for i, d in enumerate(sorted_domains)}

    # 构建 iTOL 配置内容
    output_lines = [
        "DATASET_DOMAINS",
        "SEPARATOR COMMA",
        "DATASET_LABEL,domain_structures",
        "COLOR,#ff00aa",
        "LEGEND_TITLE,Protein Domains",
        f"LEGEND_SHAPES,{','.join([domain_to_shape[d] for d in sorted_domains])}",
        f"LEGEND_COLORS,{','.join([domain_to_color[d] for d in sorted_domains])}",
        f"LEGEND_LABELS,{','.join(sorted_domains)}",
        "DATA"
    ]
    
    for gene_id, domains in protein_dict.items():
        # 计算伪长度：以最靠后的 domain 结束位置 + 20aa 作为骨架长度
        max_end = max([int(d['end']) for d in domains])
        total_len = max_end + 20
        
        domain_strings = []
        for d in domains:
            # iTOL 格式: SHAPE|START|END|COLOR|LABEL
            shape = domain_to_shape[d['label']]
            color = domain_to_color[d['label']]
            domain_strings.append(f"{shape}|{d['start']}|{d['end']}|{color}|{d['label']}")
        
        output_lines.append(f"{gene_id},{total_len},{','.join(domain_strings)}")
    
    # 写入输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(output_lines))
    
    print(f"转换成功！结果已保存至: {output_path}")
    print(f"检测到功能域: {', '.join(sorted_domains)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将基因功能域数据转换为 iTOL DATASET_DOMAINS 格式")
    parser.add_argument("-i", "--input", required=True, help="输入文件路径 (制表符分隔的 4 列格式)")
    parser.add_argument("-o", "--output", required=True, help="输出文件路径 (用于上传至 iTOL)")
    
    args = parser.parse_args()
    generate_itol_file(args.input, args.output)
