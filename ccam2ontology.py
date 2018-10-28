#! /usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import re
import urllib
import ssl
import argparse

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


parser = argparse.ArgumentParser(description='Transforme un fichier excel de la Classification Commune des Actes Médicaux (CCAM) en une ontologie de la CCAM en RDF')
parser.add_argument('fichier',nargs='?',
                    default="https://www.ameli.fr/fileadmin/user_upload/documents/CCAM_V54.10.xls",
                    help="Chemin vers un fichier excel de la CCAM fourni par l'Assurance Maladie. Si aucun fichier n'est fourni par l'utilsiateur, la version 54.10 est téléchargée depuis le site Ameli.")
args = parser.parse_args()


download_url = args.fichier
urllib.urlretrieve(download_url, "CCAM.xls")

#CCAM_xls = xlrd.open_workbook('CCAM_V41.xls')
CCAM_xls = xlrd.open_workbook('CCAM.xls')
 
CCAM = CCAM_xls.sheet_by_name(u'CCAM')

row_classe=list()
memoire_classe=None

with open('ccam.ttl','w') as CCAM_ttl:
    CCAM_ttl.write("""
@prefix ccam: <http://www.ccam.fr/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://www.ccam.fr/ontology/CCAM/> a owl:ontology ;
    rdfs:comment \"Version RDF de la Classification Commune des Actes Médicaux, fournie par l'Assurance Maladie, et transformée grâce à un script Python de Yann Rivault (https://github.com/yannrivault/CCAM_ontology)."@fr
    rdfs:label "CCAM" ;
    owl:imports <http://www.w3.org/2004/02/skos/core> .
    
""")

    for rownum in range(CCAM.nrows):
            row=CCAM.row_values(rownum)
            if isinstance(row[0], float):
                    row[0]=str(row[0])
            row[0]=row[0].replace(" ","")
            if len(row)>2:
                row[2]=row[2].replace("\"","")
            if row[0].replace(".","").isdigit() and len(row)==11 and row[3:11]==['', '', '', '', '', '', '', '']:
                memoire_classe=row[0]
                if len(row[0])==1:
                    row[0]='0'+str(row[0])
                    row_classe.append(str(row[0]))
                else:
                    row_classe.append(str(row[0]))
                CCAM_ttl.write('ccam:'+str(row[0])+' rdf:type owl:Class ;\n')
                CCAM_ttl.write('\tskos:prefLabel \"'+row[2].encode('utf-8')+'\"@fr ;\n')
                CCAM_ttl.write('\tskos:notation \"'+str(row[0])+'\"^^xsd:string ;\n')
                if row[0][:-3] in row_classe:
                    CCAM_ttl.write('\trdfs:subClassOf ccam:'+str(row[0][:-3])+' .\n')
                    CCAM_ttl.write("\n")
                if len(row[0])==3:
                    CCAM_ttl.write('\trdfs:subClassOf owl:Thing .\n')
                    CCAM_ttl.write("\n")
            elif re.match("[A-Z]{4}[0-9]{3}",row[0]):
                CCAM_ttl.write('ccam:'+row[0].encode('utf-8')+' rdf:type owl:Class ;\n')
                CCAM_ttl.write('\tskos:prefLabel \"'+row[2].encode('utf-8')+'\"\@fr ;\n')
                CCAM_ttl.write('\tskos:notation \"'+row[0].encode('utf-8')+'\"^^xsd:string ;\n')
                CCAM_ttl.write('\trdfs:subClassOf ccam:'+str(memoire_classe)+' .\n')
                CCAM_ttl.write("\n")
