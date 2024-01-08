"""Minimal working example of generating questions from a question bank.

Create five randomized versions of questions drawn from question bank A11 
to illustrate the core functionality in Ref. [1].

Call as:

$ python versions.py 

Input files
-----------
A11/
    qbank11R.tex
    qbank11C.tex
    qbank11A.tex
    qbank11U.tex


Output files
------------
A11/
    A11a/
        A11a_v0.pdf
        A11a_v1.pdf
        A11a_v2.pdf
        A11a_v3.pdf
        A11a_v4.pdf
        A11a_soln_v0.pdf
        A11a_soln_v1.pdf
        A11a_soln_v2.pdf
        A11a_soln_v3.pdf
        A11a_soln_v4.pdf
        A11a_combo.pdf
        A11a_soln_combo.pdf

Literature
----------
[1] Shepherd, T. D., and Garrett-Roe, S., J. Chem. Educ. (submitted). 

Copyright (C) 2023 Tricia D. Shepherd, Sean Garrett-Roe
"""
import subprocess, os
import random
import time

def oneattempt(numver:int,lobj:str)->None:
    """Typeset randomized assessment versions from an assessment bank.

    The function takes the number of desired versions and a string 
    indicating the question bank and version and generates multiple 
    randomized versions of questions drawn from that question bank. The 
    output files (pdfs) are saved in subfolders within the question
    bank. 

    Arguments
    ----------
    numver : int
        The number of unique versions to generate

    lobj : str
        The question bank to use with version tag, for example, the first 
        attempt at the knowledge focus 1.1 based on the assessment bank A11 
        would be `11a`

    Returns
    -------
    None
    """
    name = lobj[0]+'.'+lobj[1:] 
    obj = lobj[:-1]
    base1 = 'A'+lobj+'_v'
    base2 = 'A'+lobj+'_soln_v'
    base = [base1,base2]
    x = subprocess.call(['mkdir', 'A'+ obj + '/A'+lobj])
    for i in range(numver):
        base1 = base[0] + str(i)
        base2 = base[1] + str(i)
        fname = base1 + '.tex'
        file = open(fname,'w')
        fbank = 'A'+obj+'/qbank'+obj
        file.write('\documentclass[10pt]{exam}\n')
        file.write('\printanswers\n')
        file.write('\input{assess.sty}\n')
        file.write('\input{pyroutines.sty}\n')
        header = r'\firstpageheader{Chem 0110\\ \Large{\textbf{Assessment '
        header = header + name + '}}}{}\n'
        file.write(header)
        file.write(r'{Name:\uline{\hspace{4cm}} Peoplesoft:\uline{\hspace{3cm}}'+'\n') 
        file.write(r'\\\hspace{1cm} \\ TA: \uline{\hspace{4cm}} Day/Time: \uline{\hspace{3cm}}}'+'\n')
        header = r'\runningheader{Chem 0110\\ \Large{\textbf{Assessment '
        header = header + name + '}}}{}\n'
        file.write(header)
        file.write(r'{Name:\uline{\hspace{4cm}}}' +'\n') 
        footer = r'\firstpagefooter{\tiny{' + name + 'v' + str(i) + r' \today}}{}{}'+'\n'
        file.write(footer)
        footer = r'\runningfooter{\tiny{' + name + 'v' + str(i) + r' \today}}{}{}'+'\n'
        file.write(footer)
        file.write(r'\begin{document}'+'\n')
        infofilename = 'A'+obj+'/information.tex'
        if os.path.exists(infofilename):
            finfo = open(infofilename,'r')
            infolines = finfo.read()
            finfo.close()
            file.write(infolines)
        file.write(r'\begin{questions}'+'\n')
        flist = [fbank+'R.tex',fbank+'C.tex',fbank+'A.tex',fbank+'U.tex']
        qtype = ['Retrieval','Comprehension','Analysis','Knowledge Utilization']
        for (num,item) in enumerate(flist):
            fques = open(item,'r')
            nques = 0
            line = fques.readline()
            while line:
                if line[:12] == '\\titledquest':
                   nques = nques + 1
                line = fques.readline()
            fques.seek(0)
            nver = random.randint(1, nques)
            npick = 0
            while npick < nver:
                line = fques.readline()
                if line[:12] == '\\titledquest':
                    npick = npick + 1
            file.write('\\titledquestion{'+qtype[num]+'}\n')
            while line[:12] !='\\vspace{\\str':
                line = fques.readline()
                file.write(line)       
        file.write('\\end{questions}\n')
        file.write('\\end{document}\n')
        file.close()
        x = subprocess.run(['pdflatex', '-interaction=nonstopmode', fname])
        x = subprocess.run(['pythontex', '--runall=true',  fname])
        x = subprocess.run(['pdflatex', '-interaction=nonstopmode', fname])
        time.sleep(3)
        x = subprocess.run(['mv', base1 + '.pdf', base2 + '.pdf'])
        file = open(fname,'r')
        list_of_lines = file.readlines()
        list_of_lines[1] = "\n"
        file.close()
        file = open(fname,'w')
        file.writelines(list_of_lines)
        file.close()
        x = subprocess.run(['pdflatex', '-interaction=nonstopmode', fname])
        x = subprocess.run(['mv', base1 + '.pdf', 'A'+ obj + '/A'+lobj])
        x = subprocess.run(['mv', base2 + '.pdf', 'A'+ obj + '/A'+lobj])
        x = subprocess.run(['mv', base1 + '.tex', 'A'+ obj + '/A'+lobj])
        x = subprocess.run(['rm', '-rf', 'A'+ obj + '/A' + lobj + '/pythontex-files-' + base1])
        x = subprocess.run(['mv', 'pythontex-files-' + base1, 'A'+ obj + '/A'+lobj])
        x = subprocess.run(['rm', base1 + '.aux'])
        x = subprocess.run(['rm', base1 + '.log'])
        x = subprocess.run(['rm', base1 + '.pytxcode'])

def onecombo(numver:int,lobj:str)->None:
    """ Combine versions into a single pdf.

    The pdf's of the versions created by oneversion are combined
    into as single pdf, which is also stored in the subfolder of the
    question bank.

    Arguments
    ----------
    numver : int
        The number of unique versions to generate

    lobj : str
        The question bank to use with version tag, for example, the first 
        attempt at the knowledge focus 1.1 based on the assessment bank A11 
        would be `11a`

    Returns
    -------
    None

    """
    base1 = 'A'+lobj+'_v'
    base2 = 'A'+lobj+'_soln_v'
    base = [base1,base2]
    combo = ['A' + lobj + '_combo.tex','A' + lobj + '_soln_combo.tex']
    for i in range(2):
        file = open(combo[i],'w')
        file.write('\documentclass[11pt]{book}\n')
        file.write(r'\usepackage{pdfpages}'+'\n')
        file.write(r'\newcommand{\act}[1]{\includepdf[pages=-]{#1.pdf}}'+'\n')
        file.write(r'\begin{document}'+'\n')
        for j in range(numver):
            file.write(r'\act{A'+ lobj[:-1] + '/A'+ lobj +'/' + base[i] + str(j) + '}\n')
        file.write('\end{document}\n')
        file.close()
        x = subprocess.run(['pdflatex','-interaction=nonstopmode', combo[i]])
        x = subprocess.run(['mv', combo[i][:-4] + '.pdf', 'A'+ lobj[:-1] + '/A'+lobj])
        x = subprocess.run(['rm', combo[i][:-4] + '.aux'])
        x = subprocess.run(['rm', combo[i][:-4] + '.log'])
        x = subprocess.run(['rm', combo[i][:-4] + '.tex'])
        x = subprocess.run(['rm', combo[i][:-4] + '.synctex.gz'])


# generate 5 versions with questions from bank A11 and label it 
# the first attempt ('a') 
oneattempt(5,'11a')

# combine the created pdf files
onecombo(5,'11a')


