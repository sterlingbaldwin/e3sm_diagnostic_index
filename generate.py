import os
import sys
import argparse
import jinja2

def divide_chunks(l, n): 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def collect_case_info(input_path):
    data = []
    cases = os.listdir(input_path)
    for case in cases:
        new_data = {
            'name': case,
            'path': os.path.join(input_path, case),
            'diags': []
        }
        for diag in os.listdir(new_data['path']):
            segments = list(divide_chunks(os.listdir(os.path.join(new_data['path'], diag)), 10))
            seg1, seg2 = segments[0][0].split('-')
            freq = int(seg2) - int(seg1) + 1
            new_data['diags'].append({
                'name': diag,
                'segments': segments,
                'freq': freq
            })
        data.append(new_data)
    return data

def render_templates(data, outpath):
    templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    index_template = "index.html.j2"
    template = templateEnv.get_template(index_template)
    outputText = template.render(cases=data)

    os.makedirs(outpath, exist_ok=True)
    outpath = os.path.join(outpath, 'index.html')
    with open(outpath, 'w') as op:
        op.writelines(outputText)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inpath',  help="the top of the directory tree to discover cases in")
    parser.add_argument('-o', '--outpath', default="output", help="directory to place rendered output files default is ./output")
    args = parser.parse_args()

    data = collect_case_info(args.inpath)
    # import ipdb; ipdb.set_trace()
    render_templates(data, args.outpath)

    return 0

if __name__ == "__main__":
    sys.exit(main())