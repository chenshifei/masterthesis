This is the thesis work for the Language Technology Programm in Uppsala University.

Link to [Diva](https://www.diva-portal.org/smash/record.jsf?aq2=%5B%5B%5D%5D&c=2&af=%5B%5D&searchType=SIMPLE&sortOrder2=title_sort_asc&query=cross-lingual+word+embeddings+beyond+&language=en&pid=diva2%3A1491850&aq=%5B%5B%5D%5D&sf=all&aqe=%5B%5D&sortOrder=author_sort_asc&onlyFullText=false&noOfRows=50&dswid=6597) (Where the thesis was officially archived)

There is also a folder called `extended_abstract`, which contains this [SLTC 2020](https://spraakbanken.gu.se/en/sltc2020/program) paper of the same title.

### Abstract

    Zero-shot translation is a transfer learning setup that refers to the ability of neural machine translation to generalize translation information into unseen language pairs. It provides an appealing solution to the lack of available materials for low-resource languages by transferring knowledge from high-resource languages.

    So far, zero-shot translation mainly focuses on unseen language *pairs* whose individual component is still known to the system. There are fewer reports on transfer learning in machine translation being carried out on completely unknown test languages. This thesis pushes the boundary of zero-shot translation and explores the possibility of transferring learning from training languages to unknown test languages in a multilingual Neural Machine Translation (NMT) system.

    Based on the fact that zero-shot translation systems primarily learn language invariant features, we use cross-lingual word embeddings as the only knowledge source since they are good at capturing the semantic similarity of words from different languages in the same vector space. By conducting experiments on an encoder-decoder multilingual NMT model with an attention module, we have examined the relationship of language similarity and the transferability of unseen languages.

    We hypothesize that our multilingual NMT model with cross-lingual word embeddings should transfer reasonably even to completely unknown languages. However, we observe little transferability from the training languages to unseen test languages due to the transformed output vector space. Such minor transferability only happens between highly-related languages with a large number of shared vocabularies.
