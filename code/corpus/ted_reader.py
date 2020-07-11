import itertools
import os
import csv
from collections import defaultdict
from six.moves import zip
from argparse import ArgumentParser


class MultiLingualAlignedCorpusReader(object):
    """Handles the case of reading TED talk files
    """
    def __init__(self, corpus_path,
                 delimiter='\t',
                 word_token=False,
                 source_token=False,
                 target_token=False,
                 lang_dict={'source': ['fr'], 'target': ['en']},
                 cartesian_product=True):
        self.empty_line_flag = 'NULL'
        self.corpus_path = corpus_path
        self.delimiter = delimiter
        self.lang_dict = lang_dict
        self.lang_set = set()
        self.word_token = word_token
        self.source_token = source_token
        self.target_token = target_token
        self.cartesian_product = cartesian_product
        for list_ in self.lang_dict.values():
            for lang in list_:
                self.lang_set.add(lang)

        self.data = dict()
        self.data['train'] = self.read_aligned_corpus(split_type='train')
        self.data['test'] = self.read_aligned_corpus(split_type='test')
        self.data['dev'] = self.read_aligned_corpus(split_type='dev')

    def read_data(self, file_loc_):
        data_list = list()
        with open(file_loc_) as fp:
            for line in fp:
                try:
                    text = line.strip()
                except IndexError:
                    text = self.empty_line_flag
                data_list.append(text)
        return data_list

    def filter_text(self, dict_):
        if self.target_token and self.source_token:
            field_index = 2
        elif self.target_token or self.source_token:
            field_index = 1
        else:
            field_index = 0
        data_dict = defaultdict(list)
        list1 = dict_['source']
        list2 = dict_['target']
        for sent1, sent2 in zip(list1, list2):
            try:
                src_sent = ' '.join(sent1.split()[field_index: ])
            except IndexError:
                src_sent = 'NULL'

            if src_sent.find(self.empty_line_flag) != -1 or len(src_sent) == 0:
                continue
            elif sent2.find(self.empty_line_flag) != -1 or len(sent2) == 0:
                continue
            else:
                data_dict['source'].append(sent1)
                data_dict['target'].append(sent2)
        return data_dict

    def read_file(self, split_type, data_type):
        return self.data[split_type][data_type]

    def save_file(self, path_, split_type, data_type):
        with open(path_, 'w') as fp:
            for line in self.data[split_type][data_type]:
                fp.write(line + '\n')

    def add_word_lang_token(self, sent, lang_id):
        token = '<<' + lang_id + '>>'
        if add_to_word:
            result = [token + w for w in sent.split()]    
        return result
    
    def add_sent_lang_token(self, sent, lang_id):
        token = '__' + lang_id + '__'
        return token + ' ' + sent

    def read_from_single_file(self, path_, s_lang, t_lang):
        data_dict = defaultdict(list)
        with open(path_, 'r') as fp:
            reader = csv.DictReader(fp, delimiter='\t', quoting=csv.QUOTE_NONE)
            for row in reader:
                source_text = row[s_lang]
                if self.word_token:
                    source_text = self.add_word_lang_token(source_text, s_lang)
                if self.target_token:
                    source_text = self.add_sent_lang_token(source_text, t_lang)
                if self.source_token:
                    source_text = self.add_sent_lang_token(source_text, s_lang)
                data_dict['source'].append(source_text)
                data_dict['target'].append(row[t_lang])
        return data_dict['source'], data_dict['target']

    def read_aligned_corpus(self, split_type='train'):
        data_dict = defaultdict(list)
        if self.cartesian_product:
            iterable = itertools.product(self.lang_dict['source'],
                                         self.lang_dict['target'])
        else:
            iterable = zip(self.lang_dict['source'], self.lang_dict['target'])

        for s_lang, t_lang in iterable:
            if s_lang == t_lang:
                continue
            split_type_file_path = os.path.join(self.corpus_path, "all_talks_{}.tsv".format(split_type))
            s_list, t_list = self.read_from_single_file(split_type_file_path, s_lang=s_lang, t_lang=t_lang)
            data_dict['source'] += s_list
            data_dict['target'] += t_list
        new_data_dict = self.filter_text(data_dict)
        return new_data_dict


if __name__ == "__main__":
    parser = ArgumentParser(description='TED talks dataset reader for bilingual/multilingual translation')
    parser.add_argument('--input', '-i', type=str, default='./data/',
                        help='TED talks data directory')
    parser.add_argument('--save_data_dir', type=str, default='./data/',
                        help='directory to save translation data files')
    parser.add_argument('--src_langs', '-s',  nargs='+', type=str, default=['en'],
                        help='Source languages list (e.g. "en", "vi")')
    parser.add_argument('--tgt_langs', '-t', nargs='+', type=str, default=['vi'],
                        help='Target languages list (e.g. "en", "vi")')
    parser.add_argument('--word_token', '-wtok', action='store_true', help='Add source language token to each word in the source text, default=False')
    parser.add_argument('--src_token', '-stok', action='store_true', help='Add source language token, default=False')
    parser.add_argument('--tgt_token', '-ttok', action='store_true', help='Add target language token, default=False')
    parser.add_argument('--no_cartesian_product', '-ncp',
    dest='cartesian_product',
                        action='store_false',
                        help='Generate multilingual training data from the cartesian product of source and target language sets, default=True')
    parser.set_defaults(cartesian_product=True)
    args = parser.parse_args()

    SAVE_DATA_DIR = '{}/{}_{}'.format(args.save_data_dir, '+'.join(args.src_langs), '+'.join(args.tgt_langs))
    lang_dict={'source': args.src_langs, 'target': args.tgt_langs}

    obj = MultiLingualAlignedCorpusReader(corpus_path=args.input,
                                          lang_dict=lang_dict,
                                          source_token=args.src_token,
                                          target_token=args.tgt_token,
                                          cartesian_product=args.cartesian_product)

    os.makedirs(SAVE_DATA_DIR, exist_ok=True)
    obj.save_file(os.path.join(SAVE_DATA_DIR, 'train.src'),
                  split_type='train', data_type='source')
    obj.save_file(os.path.join(SAVE_DATA_DIR, 'train.tgt'),
                  split_type='train', data_type='target')

    obj.save_file(os.path.join(SAVE_DATA_DIR, 'test.src'),
                  split_type='test', data_type='source')
    obj.save_file(os.path.join(SAVE_DATA_DIR, 'test.tgt'),
                  split_type='test', data_type='target')

    obj.save_file(os.path.join(SAVE_DATA_DIR, 'dev.src'),
                  split_type='dev', data_type='source')
    obj.save_file(os.path.join(SAVE_DATA_DIR, 'dev.tgt'),
                  split_type='dev', data_type='target')
