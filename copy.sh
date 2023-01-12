extension="eps"

rm -rf output
mkdir output
mkdir output/cycle
mkdir output/grid_horizontal_vertical
mkdir output/grid_diagonal
mkdir output/hypercube

names=(
  "cycle/classical.${extension}"
  "cycle/hadamard.${extension}"
  "cycle/grover.${extension}"
  "cycle/dft.${extension}"
  "grid_horizontal_vertical/classical.${extension}"
  "grid_horizontal_vertical/hadamard.${extension}"
  "grid_horizontal_vertical/grover.${extension}"
  "grid_horizontal_vertical/dft.${extension}"
  "grid_diagonal/classical.${extension}"
  "grid_diagonal/hadamard.${extension}"
  "grid_diagonal/grover.${extension}"
  "grid_diagonal/dft.${extension}"
  "hypercube/classical.${extension}"
  "hypercube/hadamard.${extension}"
  "hypercube/grover.${extension}"
  "hypercube/dft.${extension}")

i=0
find ./generations/new/ -name "counts0.${extension}" | sort |
  while IFS= read -r result; do
    cp "$result" output/"${names[$i]}"
    let i++
  done


