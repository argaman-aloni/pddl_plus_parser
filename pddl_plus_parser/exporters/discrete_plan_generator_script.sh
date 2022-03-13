#!/bin/bash
directory_path="/home/mordocha/safe_action_learner/transport/"
files_regex_path="$directory_path/*.pddl"
fast_downward_dir_path="/home/mordocha/downward"
fast_downward_file_path="$fast_downward_dir_path/fast-downward.py"
domain_path="$directory_path/domain.pddl"

for FILE in $files_regex_path; do
  filename=$(basename -- "$FILE")
  name="${filename%.*}"

  echo "Processing the file - ${filename}:"
  if [[ $name == domain ]]; then
    continue
  fi
  if test -f "${directory_path}/${name}_plan.solution"; then
    continue
  else
    python "$fast_downward_file_path" --overall-time-limit "5m" --overall-memory-limit "100M" --plan-file "${directory_path}/${name}_plan.solution" "$domain_path" "$FILE" --evaluator "hff=ff()" --evaluator "hcea=cea()" --search "lazy_greedy([hff, hcea], preferred=[hff, hcea])"
    sleep 1
  fi
done
