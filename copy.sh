mkdir output
mkdir output/cycle
mkdir output/grid_horizontal_vertical
mkdir output/grid_diagonal
mkdir output/hypercube

names=(
  "cycle/classical.eps"
  "cycle/hadamard.eps"
  "cycle/grover.eps"
  "cycle/dft.eps"
  "grid_horizontal_vertical/classical.eps"
  "grid_horizontal_vertical/hadamard.eps"
  "grid_horizontal_vertical/grover.eps"
  "grid_horizontal_vertical/dft.eps"
  "grid_diagonal/classical.eps"
  "grid_diagonal/hadamard.eps"
  "grid_diagonal/grover.eps"
  "grid_diagonal/dft.eps"
  "hypercube/classical.eps"
  "hypercube/hadamard.eps"
  "hypercube/grover.eps"
  "hypercube/dft.eps")

i=0
while IFS= read -r result; do
  cp "$result" output/"${names[$i]}"
  let i++
done

# find ./generations/new/ -name "counts0.eps" | sort | ./copy.sh

