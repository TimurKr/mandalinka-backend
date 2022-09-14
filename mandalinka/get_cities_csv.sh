#!/bin/bash
if [ $# -ne 0 ];then
	if [ ${1##*.} == "txt" ] || [[ ${1##*.} == "csv" ]]; then
		touch $PWD/$1;
		file=$PWD/$1;
		echo "Writing into given file $PWD/$1";
	fi
else
	touch  $PWD/city_street_postal_dpost_distr.csv;
	file=$PWD/city_street_postal_dpost_distr.csv;
	echo "Writing into file $file";
fi

echo "OBEC; ULICA; PSC; DPOSTA; OKRES" > ${file}

for region in "banskobystricky"  "bratislavsky"  "kosicky"  "nitriansky"  "presovsky"  "trnciansky"  "trnavsky"  "zilinsky"; do
	curl www.psc.vsetko.info/$region.php  | tr -d "\r\n" | grep -o "<tbody>.*</tbody>" | sed "s#</tr>#</tr>|#g" | tr "|" "\n"  | sed 's/    //g' | sed 's/<tr><td>//g' | sed 's#</td><td>#;#g' | sed 's#</td>  </tr>##g' | sed "s/<t*body>//g" | sed "s#</tbody>##g"  >> ${file};
done
sed -i "/^$/d" $file
