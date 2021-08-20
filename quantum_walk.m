tic;
n = 100
N = n*n
steps = 1000

start_pos = sparse(zeros(1,N));
start_pos(floor(N/2)+1) = 1;
start_coin = sparse(kron([1/sqrt(2),1i/sqrt(2)], [1/sqrt(2), 1i/sqrt(2)]))

shift_left = sparse(zeros(N,N));
shift_right = sparse(zeros(N,N));
shift_down = sparse(zeros(N,N));
shift_up = sparse(zeros(N,N));

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

% 1. érme: y
% 2. érme: x
% [1,0,0,0] = kron([1,0],[1,0]) up & left -> left
% [0,1,0,0] = kron([1,0],[0,1]) up & right -> right
% [0,0,1,0] = kron([0,1],[1,0]) down & left -> down
% [0,0,0,1] = kron([0,1],[0,1]) down & right -> up

S = kron(shift_up * shift_left, [1,0,0,0]' * [1,0,0,0]) + ...
kron(shift_up * shift_right, [0,1,0,0]' * [0,1,0,0]) + ...
kron(shift_down * shift_left, [0,0,1,0]' * [0,0,1,0]) + ...
kron(shift_down * shift_right, [0,0,0,1]' * [0,0,0,1]);

I = speye(N);
C = sparse(hadamard(4) / 2);
U = S * kron(I, C);

start= kron(start_pos, start_coin);

result = (U^steps*start')';


%prob = zeros(1,N);
%for k=1:N
%  posn = zeros(1,N);
%  posn(1,k) = 1;
%  M_hat_k = kron(posn'*posn, eye(4));
%  proj = M_hat_k * result';
%  prob(1,k) = proj'*proj;
%end

%plane = reshape(prob,[n,n]);

%figure
%surf(plane)
toc;

function ret = step2d(i, stepx, stepy, n)
  i_x = mod(i,n);
  i_y = floor(i/n);
  
  ret_x = mod(i_x+stepx, n);
  ret_y = mod(i_y+stepy, n);
  ret = ret_y * n + ret_x;
end