import os

def imenice(korpus):
	rečnik = dict()

	# lista fajlova SrpLemKor-a osim 260, 4505, 4517 koji izbacuju grešku u encoding-u
	folder_korpusa = os.path.join(".", korpus, "texts", "")
	fajlovi = [f for f in os.listdir(folder_korpusa) if f not in ["260.txt", "4505.txt","4517.txt"]]

	# prolazi fajlove korpusa
	for f in fajlovi:
		with open(folder_korpusa + f) as korpus:
			for red in korpus:
				entry = red.strip().split("\t")
				pos = entry[6]

				# izbacuje reči za koje u korpusu ne postoji određena lema
				try:
					lemma = entry[7]
					if lemma == lemma.lower():
						lemma = lemma.replace("cx", "ć").replace("cy", "č").replace("dx", "đ").replace("dy", "dž").replace("lx", "lj").replace("nx", "nj").replace("sx", "š").replace("zx", "ž")

						if pos.startswith('N') and "@" not in lemma and "<" not in lemma:
							try:
								rečnik[lemma] += 1
							except:
								rečnik[lemma] = 1
				except:
					pass

	sorted_by_value = sorted(rečnik.items(), key=lambda kv: kv[1])

	with open("imenice.txt", "w", encoding="utf-8") as imenice_po_frekvenci:
		for reč, frekvenca in sorted_by_value:
			imenice_po_frekvenci.write(str(reč) + "\n")

def glagoli(korpus):
	rečnik = dict()

	# lista fajlova SrpLemKor-a osim 260, 4505, 4517 koji izbacuju grešku u encoding-u
	folder_korpusa = os.path.join(".", korpus, "texts", "")
	fajlovi = [f for f in os.listdir(folder_korpusa) if f not in ["260.txt", "4505.txt","4517.txt"]]

	# prolazi fajlove korpusa
	for f in fajlovi:
		with open(folder_korpusa + f) as korpus:
			for red in korpus:
				entry = red.strip().split("\t")
				pos = entry[6]

				# izbacuje reči za koje u korpusu ne postoji određena lema
				try:
					lemma = entry[7]
					if lemma == lemma.lower():
						lemma = lemma.replace("cx", "ć").replace("cy", "č").replace("dx", "đ").replace("dy", "dž").replace("lx", "lj").replace("nx", "nj").replace("sx", "š").replace("zx", "ž")

						if pos.startswith('V') and "@" not in lemma and "<" not in lemma:
							try:
								rečnik[lemma] += 1
							except:
								rečnik[lemma] = 1
				except:
					pass

	sorted_by_value = sorted(rečnik.items(), key=lambda kv: kv[1])

	with open("glagoli.txt", "w", encoding="utf-8") as imenice_po_frekvenci:
		for reč, frekvenca in sorted_by_value:
			imenice_po_frekvenci.write(str(reč) + "\n")