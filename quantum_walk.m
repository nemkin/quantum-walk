n = 25
N = n*n
steps = 25

start_pos = zeros(1,N);
start_pos(floor(N/2)+1) = 1;
start_coin = [1/2,i/2,i/2,-1/2];

shift_left = zeros(N,N);
shift_right = zeros(N,N);
shift_down = zeros(N,N);
shift_up = zeros(N,N);

for i=0:N-1
  left = step2d(i, -1, 0, n);
  right = step2d(i, 1, 0, n);
  down = step2d(i, 0, -1, n);
  up = step2d(i, 0, 1, n);
  
  shift_left(left+1, i+1) = shift_left(left+1, i+1) + 1;
  shift_right(right+1, i+1) = shift_right(right+1, i+1) + 1;
  shift_down(down+1, i+1) = shift_down(down+1, i+1) + 1;
  shift_up(up+1, i+1) = shift_up(up+1, i+1) + 1;
end

S = kron(shift_left, [1,0,0,0]'*[1,0,0,0]) + ...
    kron(shift_right, [0,1,0,0]'*[0,1,0,0]) + ...
    kron(shift_down, [0,0,1,0]'*[0,0,1,0]) + ...
    kron(shift_up, [0,0,0,1]'*[0,0,0,1]);

I = eye(N);
C = hadamard(4) / 2;
U = S * kron(I, C);
start = kron(start_pos, start_coin);
result = (U^steps*start')';

prob = zeros(1,N);
for k=1:N
  posn = zeros(1,N);
  posn(1,k) = 1;
  M_hat_k = kron(posn'*posn, eye(4));
  proj = M_hat_k * result';
  prob(1,k) = proj'*conj(proj);
end

plane = reshape(prob,[n,n])

figure
surfl(plane)

function ret = step2d(i, stepx, stepy, n)
  i_x = mod(i,n);
  i_y = floor(i/n);
  
  ret_x = mod(i_x+stepx, n);
  ret_y = mod(i_y+stepy, n);
  ret = ret_y * n + ret_x;
end