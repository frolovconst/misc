import re
import sys
import subprocess
from os import listdir

def replace_all_matches_in_line(regex, line):
    search_result = regex.search(line)
    while search_result is not None:
        matched_fragment = search_result[0]
        new_fragment = matched_fragment.replace('\"', '\'')
        line = line.replace(matched_fragment, new_fragment)
        search_result = regex.search(line)
    return line

def replace_single_quotes_in_file(path, restore_sngl_quote_re):
    with open(path, 'r', encoding='unicode_escape') as src_file:
        dst_file_path = path[:-4]+'_mdf.txt'
        with open(dst_file_path, 'w', encoding='utf-8') as dst_file:
            gen = get_file_iterator(src_file)
            for src_line in gen:
                quote = src_line.replace('\'', '\"')
                quote = replace_all_matches_in_line(restore_sngl_quote_re, quote)
                dst_file.write(quote)
    return dst_file_path
            
def get_file_iterator(file):
    for line in file:
        yield line #.readline()    
        
def process_line(line):
    result = line.split('Text="')
    if len(result) < 2:
        return None
    else:
        result = result[1]
    result = result.split('", Speaker=')
    if len(result) < 2:
        return None
    else:
        speaker = result[1].split(']')[0]
    return result[0] + ' (' + speaker + ')'

def exec_bash_command(bashCommand):
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

        
if __name__ == '__main__':
    restore_sngl_quote_re = re.compile("([A-Za-z]\"[A-Za-z])|([A-Za-z][^\.\?!,]\")")
    formatted_file_name = replace_single_quotes_in_file(sys.argv[1], restore_sngl_quote_re)
    bashCommand = f'java -Xmx40g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,depparse,coref,quote -file {formatted_file_name} -outputFormat text'
    exec_bash_command(bashCommand)
    with open(formatted_file_name + '.out', encoding='utf-8') as src_file, \
        open('quotes.txt', 'w', encoding='utf-8') as dst_file:
        gen = get_file_iterator(src_file)
        for i in gen:
            if i.startswith('Extracted quotes:'):
                break
        for i in gen:
            quote = process_line(i)
            if quote is None:
                continue
            quote += '\n'
            dst_file.write(quote)
