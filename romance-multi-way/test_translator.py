import subprocess


def main():
	target_lan = input("Target Language: ")
	model_file = ""
	if target_lan in ["es", "fr", "it", "ro"]:
		model_file = "pt_{}/model/model_pt_{}_checkpoint.t7".format(target_lan, target_lan)
	else:
		print("Not implemented!")
		exit(1)

	bpe_model = "pt_{}/data/esfritptro.bpe32000".format(target_lan)

	input_sentences = "input_sentences.txt"
	input_tok = "input_sentences.tok"

	output_senteces = "output_senteces.txt"
	output_tok = "input_sentences_out.tok"

	cmd = 'th tools/tokenize.lua -case_feature -joiner_annotate -nparallel 4 -bpe_model {} < {} > {}'.format(
		bpe_model,
		input_sentences,
		input_tok
	)
	print("Tokenizing...")
	print("cmd: ", cmd)
	subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

	print("Adding target language...")
	cmd = 'perl -i.bak -pe "s//__opt_tgt_{}\xEF\xBF\xA8N /" {}'.format(target_lan, input_tok)
	subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

	print("Translating...")
	cmd = 'th translate.lua -replace_unk -model {} -src {} -output {} -gpuid 1'.format(model_file, input_tok, output_tok)
	print("cmd: ", cmd)
	subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

	print("Detokenizing...")
	cmd = 'th tools/detokenize.lua -nparallel 4 < {} > {}'.format(output_tok, output_senteces)
	print("cmd: ", cmd)
	subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)


if __name__ == '__main__':
	main()
