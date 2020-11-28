import json 
import argparse



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file') 
    parser.add_argument('-o')
    
    args = parser.parse_args()
    reddits = []
    with open(args.input_file, 'r') as f: 
        for line in f:
            reddits.append(json.loads(line))
#    print(reddits)
    
    filtered = []  
    for line in reddits:        
        if 'trump' in  line['title'].lower() or 'biden' in line['title'].lower():
            filtered.append(line)        
    
    with open(args.o,'w') as fh:
        for j in range(len(filtered)):
            json.dump(filtered[j], fh)
            fh.write('\n')

if __name__ == '__main__':
    main() 
