import re

def alomorf(prefiks, reč): 
    """
    Proverava da li je zadovoljen uslov okruženja za javljanje određenih alomorfa.
    """
    lista_prefiksa_s_uslovima = ['is', 'us', 'ras', 'nus', 'bes', 'op', 'ot', 'pot', 'nat', 'pret', 'z', 'iš', 'raš', 'š', 'iž', 'ž', 'iza', 'raza', 'oda']
    lista_prefiksa_bez_uslova = ['protiv', 'polu', 'pred', 'samo', 'mimo', 'među', 'bez', 'van', 'pod', 'pra', 'pre', 'pri', 'raz', 'nad', 'nuz', 'po', 'do', 'iz', 'uz', 'na', 'ne', 'su', 'sa', 'od', 'za', 'ob', 'o', 'u', 's']
    s_tip = ['is', 'us', 'ras', 'nus', 'bes', 'pret', 'ot', 'pot', 'nat', 'op']
    š_tip = ['iš', 'raš', 'š']
    ž_tip = ['iž', 'š']
    a_tip = ['iza', 'raza', 'oda']

    if prefiks in lista_prefiksa_s_uslovima and len(reč[len(prefiks):]) > 1:
        if prefiks in s_tip and re.match('[ptkhfcč]', reč[len(prefiks):]):
            return True
        elif prefiks == 'z' and re.match('[bdg]', reč[len(prefiks):]):
            return True
        elif prefiks in š_tip and re.match('[čć]', reč[len(prefiks):]):
            return True
        elif prefiks in ž_tip and re.match('[dž|đ]', reč[len(prefiks):]):
            return True
        elif prefiks in a_tip and re.findall('[zbsš]', reč[len(prefiks):]):
            return True
    elif prefiks in lista_prefiksa_bez_uslova:
        return True
    else:
        return False

def provera_glagola(osnova_bez_sufiksa, lista_infinitiva, uslov, lista_glagola, lista_prefiksa, gpt_check):
    """
    Proverava da li imenice koje su nastale od glagolskog prideva trpnog zadovoljavaju peti odnosno šesti uslov.
    """
    for nastavak_za_infinitiv in lista_infinitiva:
        potencijalni_glagol = osnova_bez_sufiksa + nastavak_za_infinitiv
        if potencijalni_glagol in lista_glagola:
            prvi = prvi_uslov(potencijalni_glagol, prefiks, lista_glagola)
            if prvi == 0:
                drugi = drugi_uslov(prefiks, potencijalni_glagol, lista_prefiksa, lista_glagola)

            """
            Za objašnjenje gpt_check, vidi linije 133-4.
            """
            if gpt_check == False:
                if prvi == 1:
                    uslov = 3
                elif drugi == 2:
                    uslov = 4
            elif gpt_check == True:
                if prvi == 1:
                    uslov = 5
                elif drugi == 2:
                    uslov = 6
            return uslov
            break
    if uslov != 3 and uslov != 4 and uslov != 5 and uslov != 6:
        return 0

def prvi_uslov(reč, prefiks, rečnik):
    """
    Proverava da li se potencijalna osnova nalazi u rečniku.
    Isključuje sve kratke nizove (npr. 'sa', gde bi se 's-' se prepoznalo kao prefiks a '-a' kao reč srpskog jezika).         
    """
    if reč[len(prefiks):] in rečnik and len(reč[len(prefiks):]) > 1:
        return 1
    else:
        return 0

def drugi_uslov(prefiks, reč, lista_prefiksa, rečnik):
    global prefiks2
    """
    Proverava da li se na potencijalnu osnovu moze dodati drugi prefiks tako da dobijena reč bude leksikalizovana.         
    """
    uslov = 0
    for prefiks2 in lista_prefiksa:
        if prefiks2 + reč[len(prefiks):] in rečnik and prefiks != prefiks2 and len(reč[len(prefiks):]) > 1 and len(reč[len(prefiks2):]) > 1 and alomorf(prefiks2, reč) == True: #treći uslov u if petlji: ne zelimo da se prefiks menja samim sobom.
            uslov = 2
            return uslov
            break
    if uslov == 0:
        return 0


def prefiksator(reč, lista_prefiksa, rečnik, lista_sufiksa, lista_infinitiva, lista_glagola, lj_lista):
    global uslov, prefiks, prefiks2, sufiks, potencijalni_glagol
    """
    startswith_check je promenljiva koja prati da li ijedan prefiks (uz alomorfska pravila) odgovara početku reči; služi da bi se u uslov_0.txt našle samo reči poput 'sako' (sa-), ali ne i 'pšenica' (pš-???)
    """
    startswith_check = False

    for prefiks in lista_prefiksa:
        gpt_check = False
        """
        uslov je promenljiva koja prati da li je zadovoljen neki od uslova da se slovni niz smatra prefiksom
        """
        uslov = 0 

        if reč.startswith(prefiks) and alomorf(prefiks, reč) == True:
            startswith_check = True
            
            """
            Provera prvog uslova
            """
            uslov = prvi_uslov(reč, prefiks, rečnik)
            if uslov == 1:
                with open('uslov_1.txt', 'a+', encoding = 'utf-8') as izlaz_1:
                    izlaz_1.write(reč + ' : ' + prefiks + '\n')
                    break

            else:
                """
                Provera drugog uslova
                """
                uslov = drugi_uslov(prefiks, reč, lista_prefiksa, rečnik)
                if uslov == 2:
                    with open('uslov_2.txt', 'a+', encoding = 'utf-8') as izlaz_2:
                        izlaz_2.write(reč + ' : ' + prefiks + ' (' + prefiks2 + ')\n')
                        break

                else:
                    """
                    Proverava da li se reč završava na sufiks(e) (može da prepozna da se reč završava na više sufiksa, npr. -ijacija i -a)
                    """
                    lista_sufiksa_za_pojedinačnu_reč = list() 
                    for sufiks in lista_sufiksa:
                        if reč.endswith(sufiks):
                            lista_sufiksa_za_pojedinačnu_reč.append(sufiks)

                    """
                    Za svaki od potencijalno prisutnih sufiksa proverava da li neki uslov može da se zadovolji
                    """
                    for sufiks in lista_sufiksa_za_pojedinačnu_reč:
                        """
                        gpt_check je promenljiva koja odlučuje da li će funkcija provera_glagola proveravati za 3. i 4., ili za 5. i 6. pravilo
                        gpt_check daje odgovor na pitanje "da li program trenutno proverava 5. i 6. pravilo?"
                        """
                        gpt_check = False

                        osnova_bez_sufiksa = reč[:(-len(sufiks))]
                        uslov = provera_glagola(osnova_bez_sufiksa, lista_infinitiva, uslov, lista_glagola, lista_prefiksa, gpt_check)
                        
                        """
                        Ako nije zadovoljen ni treći ni četvrti uslov, prelazi se na peti i šesti:
                        """
                        if uslov == 0:
                            gpt_check = True

                            """
                            Ako je u pitanju neki od sufiksa koji su se stopili sa nastavkom za građenje gpt, program ovde vraća to 'n' na osnovu.
                            """
                            if sufiks.startswith('n'):
                                osnova_bez_sufiksa = osnova_bez_sufiksa + 'n'

                            if osnova_bez_sufiksa.endswith('nut') or osnova_bez_sufiksa.endswith('at'):
                                osnova_bez_sufiksa = osnova_bez_sufiksa[:-1]
                                uslov = provera_glagola(osnova_bez_sufiksa, lista_infinitiva, uslov, lista_glagola, lista_prefiksa, gpt_check)

                            elif osnova_bez_sufiksa.endswith('an'):
                                osnova_bez_sufiksa = osnova_bez_sufiksa[:-1]
                                uslov = provera_glagola(osnova_bez_sufiksa, lista_infinitiva, uslov, lista_glagola, lista_prefiksa, gpt_check)

                            elif osnova_bez_sufiksa.endswith('en'):
                                osnova_bez_sufiksa = osnova_bez_sufiksa[:-2]
                                uslov = provera_glagola(osnova_bez_sufiksa, lista_infinitiva, uslov, lista_glagola, lista_prefiksa, gpt_check)
                                for jotovano in lj_lista:
                                    if osnova_bez_sufiksa.endswith(jotovano):
                                        osnova_bez_sufiksa = osnova_bez_sufiksa[:-2]
                                        uslov = provera_glagola(osnova_bez_sufiksa, lista_infinitiva, uslov, lista_glagola, lista_prefiksa, gpt_check)
                                if osnova_bez_sufiksa.endswith('đ'):
                                    osnova_bez_sufiksa = osnova_bez_sufiksa[:-1] + 'd'
                                    uslov = provera_glagola(osnova_bez_sufiksa, lista_infinitiva, uslov, lista_glagola, lista_prefiksa, gpt_check)
                                elif osnova_bez_sufiksa.endswith('ć'):
                                    osnova_bez_sufiksa = osnova_bez_sufiksa[:-1] + 't'
                                    uslov = provera_glagola(osnova_bez_sufiksa, lista_infinitiva, uslov, lista_glagola, lista_prefiksa, gpt_check)
                                elif osnova_bez_sufiksa.endswith('šlj'):
                                    osnova_bez_sufiksa = osnova_bez_sufiksa[:-3] + 'sl'
                                    uslov = provera_glagola(osnova_bez_sufiksa, lista_infinitiva, uslov, lista_glagola, lista_prefiksa, gpt_check)
                                elif osnova_bez_sufiksa.endswith('j'):
                                    osnova_bez_sufiksa = osnova_bez_sufiksa[:-1]
                                    uslov = provera_glagola(osnova_bez_sufiksa, lista_infinitiva, uslov, lista_glagola, lista_prefiksa, gpt_check)
                                elif osnova_bez_sufiksa.endswith('š'):
                                    osnova_bez_sufiksa = osnova_bez_sufiksa[:-1] + 's'
                                    uslov = provera_glagola(osnova_bez_sufiksa, lista_infinitiva, uslov, lista_glagola, lista_prefiksa, gpt_check)
                                elif osnova_bez_sufiksa.endswith('č'):
                                    osnova_bez_sufiksa = osnova_bez_sufiksa[:-1] + 'c'
                                    uslov = provera_glagola(osnova_bez_sufiksa, lista_infinitiva, uslov, lista_glagola, lista_prefiksa, gpt_check)
                                elif osnova_bez_sufiksa.endswith('č'):
                                    osnova_bez_sufiksa = osnova_bez_sufiksa[:-1]
                                    lista_infinitiva_ći = ['ći']
                                    uslov = provera_glagola(osnova_bez_sufiksa, lista_infinitiva_ći, uslov, lista_glagola, lista_prefiksa, gpt_check)

                        """
                        Naredni if/elif upisuje ako je neki uslov zadovoljen i breakuje for za odabrani sufiks iz liste sufiksa, dakle prelazi na sledeću reč.
                        """
                        if uslov == 3:
                            with open('uslov_3.txt', 'a+', encoding = 'utf-8') as izlaz_3:
                                izlaz_3.write(reč + ' : ' + prefiks + ' : ' + sufiks + '\n')
                                break
                        elif uslov == 4:
                            with open('uslov_4.txt', 'a+', encoding = 'utf-8') as izlaz_4:
                                izlaz_4.write(reč + ' : ' + prefiks + ' : ' + sufiks + '\n')
                                break
                        elif uslov == 5:
                            with open('uslov_5.txt', 'a+', encoding = 'utf-8') as izlaz_5:
                                izlaz_5.write(reč + ' : ' + prefiks + ' : ' + sufiks + '\n')
                                break
                        elif uslov == 6:
                            with open('uslov_6.txt', 'a+', encoding = 'utf-8') as izlaz_6:
                                izlaz_6.write(reč + ' : ' + prefiks + ' : ' + sufiks + '\n')  
                                break
    
    """
    Ukoliko reč nije zadovoljila nijedan uslov (uslov == 0), a počinje slovnim nizom koji je jednak nekom od prefiksa (startswith_check == True), program je izbacuje u uslov_0.txt
    """
    if uslov == 0 and startswith_check == True:
        with open('uslov_0.txt', 'a+', encoding = 'utf-8') as izlaz_0:
            izlaz_0.write(reč + '\n')  