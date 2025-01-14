#!/bin/bash

# Declare a string array with type
declare -a TablesArray=(
    "gap_powerbioptionsetrefs"
    "kc_interviews"
    "leads"
    "opportunities"
    "rn_stagehistories"
    "systemusers"
    "businessunits"
    "accounts"
    "opportunitysalesprocesses"
    "processstages"
    "teams",
    "rn_tenderplatforms"
)

csv_path="${XL_IDP_PATH_CRM}"

done_path="${csv_path}"/done
if [ ! -d "$done_path" ]; then
  mkdir "${done_path}"
fi

json_path="${csv_path}"/json
if [ ! -d "$json_path" ]; then
  mkdir "${json_path}"
fi


for table in "${TablesArray[@]}"; do
  find "${csv_path}" -maxdepth 1 -type f \( -name "${table}.csv" \) ! -newermt '3 seconds ago' -print0 | while read -d $'\0' file
  do

    if [[ "${file}" == *"error_"* ]];
    then
      continue
    fi

    mime_type=$(file -b --mime-type "$file")
    echo "'${file} - ${mime_type}'"


    python3 "${XL_IDP_ROOT_CRM}/scripts/${table}.py" "${file}" "${json_path}"

    if [ $? -eq 0 ]
    then
      mv "${file}" "${done_path}"
    else
      echo "ERROR during convertion ${file} to csv!"
      mv "${file}" "${csv_path}/error_$(basename "${file}")"
      continue
    fi

  done

done