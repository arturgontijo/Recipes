#!/bin/bash
if [ -z "$1" ] || [ -z "$2" ]
  then
    echo "Invalid arguments: ./run_translator.sh SOURCE_LANGUAGE TARGET_LANGUAGE"
    exit 1
fi

file="data/$1$2.bpe32000"
if [ -f "$file" ]
then
	th ./OpenNMT/tools/tokenize.lua -case_feature -joiner_annotate -nparallel 4 -bpe_model data/$1$2.bpe32000 < input_sentences.txt > input.tok
else
    file="data/$2$1.bpe32000"
    if [ -f "$file" ]
    then
	    th ./OpenNMT/tools/tokenize.lua -case_feature -joiner_annotate -nparallel 4 -bpe_model data/$2$1.bpe32000 < input_sentences.txt > input.tok
	else
	    echo "BPE ($file) not found, exiting.."
	    exit 1
	fi
fi

perl -i.bak -pe "s//__opt_tgt_$2\xEF\xBF\xA8N /" input.tok

file="data/model_$1$2.t7"
if [ -f "$file" ]
then
	th ./OpenNMT/translate.lua -replace_unk -model data/model_$1$2.t7 -src input.tok -output output.tok -gpuid 1
else
    file="data/model_$2$1.t7"
    if [ -f "$file" ]
    then
	    th ./OpenNMT/translate.lua -replace_unk -model data/model_$2$1.t7 -src input.tok -output output.tok -gpuid 1
	else
	    echo "Model ($file) not found, exiting.."
	    exit 1
	fi
fi

th ./OpenNMT/tools/detokenize.lua -nparallel 4 < output.tok > output_sentences.txt
rm input.tok*
rm output.tok
