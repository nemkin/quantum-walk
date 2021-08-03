n = 25
N = n*n
steps = 25

start_pos = zeros(1,N);
start_pos(floor(N/2)+1) = 1;
% start_coin = [1/2,i/2,i/2,-1/2];
start_coin_1 = [1,0,0,0]
start_coin_4 = [0,0,0,1]

% 1. érme: y
% 2. érme: x
% [1,0,0,0] = kron([1,0],[1,0])
% [0,1,0,0] = kron([1,0],[0,1])
% [0,0,1,0] = kron([0,1],[1,0])
% [0,0,0,1] = kron([0,1],[0,1])

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

S_x = kron(shift_left, [1,0,0,0]'*[1,0,0,0]) + ...
    kron(shift_right, [0,1,0,0]'*[0,1,0,0])
    
S_y =kron(shift_down, [0,0,1,0]'*[0,0,1,0]) + ...
    kron(shift_up, [0,0,0,1]'*[0,0,0,1]);

I = eye(N);

C = hadamard(2) / sqrt(2);
I_2 = eye(2)

C_x = kron(C, I_2)
C_y = kron(I_2, C)

U = S_x * kron(I, C_x) + S_y * kron(I, C_y);

start_1 = kron(start_pos, start_coin_1);
start_4 = kron(start_pos, start_coin_4);

result_1 = (U^steps*start_1')';
result_4 = (U^steps*start_4')';

prob_1 = zeros(1,N);
for k=1:N
  posn = zeros(1,N);
  posn(1,k) = 1;
  M_hat_k = kron(posn'*posn, eye(4));
  proj = M_hat_k * result_1';
  prob_1(1,k) = proj'*proj;
end

prob_4 = zeros(1,N);
for k=1:N
  posn = zeros(1,N);
  posn(1,k) = 1;
  M_hat_k = kron(posn'*posn, eye(4));
  proj = M_hat_k * result_4';
  prob_4(1,k) = proj'*proj;
end

plane_1 = reshape(prob_1,[n,n]);
plane_4 = reshape(prob_4,[n,n]);

plane_4_step_1 = flip(plane_4)
plane_4_step_2 = plane_4_step_1'
plane_4_flipped = flip(plane_4_step_2)

isequal(plane_1, plane_4_flipped)

figure
surf(plane_1)

figure
surf(plane_4_flipped)

figure
surf(plane_1-plane_4_flipped)

function ret = step2d(i, stepx, stepy, n)
  i_x = mod(i,n);
  i_y = floor(i/n);
  
  ret_x = mod(i_x+stepx, n);
  ret_y = mod(i_y+stepy, n);
  ret = ret_y * n + ret_x;
end