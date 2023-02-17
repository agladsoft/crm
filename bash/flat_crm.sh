#!/bin/bash

csv_path="${XL_IDP_PATH_CRM}/crm"

done_path="${csv_path}"/done
if [ ! -d "$done_path" ]; then
  mkdir "${done_path}"
fi

json_path="${csv_path}"/json
if [ ! -d "$json_path" ]; then
  mkdir "${json_path}"
fi



find "${csv_path}" -maxdepth 1 -type f \( -name "gap_powerbioptionsetrefs.csv" \) ! -newermt '3 seconds ago' -print0 | while read -d $'\0' file
do

  if [[ "${file}" == *"error_"* ]];
  then
    continue
  fi

	mime_type=$(file -b --mime-type "$file")
  echo "'${file} - ${mime_type}'"


  python3 ${XL_IDP_ROOT_CRM}/scripts/gap_powerbioptionsetrefs.py "${file}" "${json_path}"

  if [ $? -eq 0 ]
	then
	  mv "${file}" "${done_path}"
	else
	  echo "ERROR during convertion ${file} to csv!"
	  mv "${file}" "${csv_path}/error_$(basename "${file}")"
	  continue
	fi

done



find "${csv_path}" -maxdepth 1 -type f \( -name "kc_interviews.csv" \) ! -newermt '3 seconds ago' -print0 | while read -d $'\0' file
do

  if [[ "${file}" == *"error_"* ]];
  then
    continue
  fi

	mime_type=$(file -b --mime-type "$file")
  echo "'${file} - ${mime_type}'"


  python3 ${XL_IDP_ROOT_CRM}/scripts/kc_interviews.py "${file}" "${json_path}"

  if [ $? -eq 0 ]
	then
	  mv "${file}" "${done_path}"
	else
	  echo "ERROR during convertion ${file} to csv!"
	  mv "${file}" "${csv_path}/error_$(basename "${file}")"
	  continue
	fi

done




find "${csv_path}" -maxdepth 1 -type f \( -name "leads.csv" \) ! -newermt '3 seconds ago' -print0 | while read -d $'\0' file
do

  if [[ "${file}" == *"error_"* ]];
  then
    continue
  fi

	mime_type=$(file -b --mime-type "$file")
  echo "'${file} - ${mime_type}'"


  python3 ${XL_IDP_ROOT_CRM}/scripts/leads.py "${file}" "${json_path}"

  if [ $? -eq 0 ]
	then
	  mv "${file}" "${done_path}"
	else
	  echo "ERROR during convertion ${file} to csv!"
	  mv "${file}" "${csv_path}/error_$(basename "${file}")"
	  continue
	fi

done





find "${csv_path}" -maxdepth 1 -type f \( -name "opportunities.csv" \) ! -newermt '3 seconds ago' -print0 | while read -d $'\0' file
do

  if [[ "${file}" == *"error_"* ]];
  then
    continue
  fi

	mime_type=$(file -b --mime-type "$file")
  echo "'${file} - ${mime_type}'"


  python3 ${XL_IDP_ROOT_CRM}/scripts/opportunities.py "${file}" "${json_path}"

  if [ $? -eq 0 ]
	then
	  mv "${file}" "${done_path}"
	else
	  echo "ERROR during convertion ${file} to csv!"
	  mv "${file}" "${csv_path}/error_$(basename "${file}")"
	  continue
	fi

done




find "${csv_path}" -maxdepth 1 -type f \( -name "rn_stagehistories.csv" \) ! -newermt '3 seconds ago' -print0 | while read -d $'\0' file
do

  if [[ "${file}" == *"error_"* ]];
  then
    continue
  fi

	mime_type=$(file -b --mime-type "$file")
  echo "'${file} - ${mime_type}'"


  python3 ${XL_IDP_ROOT_CRM}/scripts/rn_stagehistories.py "${file}" "${json_path}"

  if [ $? -eq 0 ]
	then
	  mv "${file}" "${done_path}"
	else
	  echo "ERROR during convertion ${file} to csv!"
	  mv "${file}" "${csv_path}/error_$(basename "${file}")"
	  continue
	fi

done





find "${csv_path}" -maxdepth 1 -type f \( -name "systemusers.csv" \) ! -newermt '3 seconds ago' -print0 | while read -d $'\0' file
do

  if [[ "${file}" == *"error_"* ]];
  then
    continue
  fi

	mime_type=$(file -b --mime-type "$file")
  echo "'${file} - ${mime_type}'"


  python3 ${XL_IDP_ROOT_CRM}/scripts/systemusers.py "${file}" "${json_path}"

  if [ $? -eq 0 ]
	then
	  mv "${file}" "${done_path}"
	else
	  echo "ERROR during convertion ${file} to csv!"
	  mv "${file}" "${csv_path}/error_$(basename "${file}")"
	  continue
	fi

done