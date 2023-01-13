extension="png"

rm -rf output
mkdir output

i=2
find ./generations/new/ -name "counts0.${extension}" | sort |
  while IFS= read -r result; do
    echo $i
    file=$(basename $result)
    cp "$result" output/"${i}_$file"
    echo "$result" output/"${i}_$file"
    let i++
  done

i=2
find ./generations/new/ -name "periodicity.txt" | sort |
  while IFS= read -r result; do
    echo $i
    file=$(basename $result)
    cp "$result" output/"${i}_$file"
    echo "$result" output/"${i}_$file"
    let i++
  done


