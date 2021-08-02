n = 3
N = n*n
steps = 100

start_pos = zeros(1,N);
start_pos(floor(N/2)+1) = 1;
start_coin = [1,0,0,0];

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

I_4 = eye(4);


S = kron(shift_left, I_4(1,:)'*I_4(1,:)) + ...
    kron(shift_right, I_4(2,:)'*I_4(2,:)) + ...
    kron(shift_down, I_4(3,:)'*I_4(3,:)) + ...
    kron(shift_up, I_4(4,:)'*I_4(4,:));

I = eye(N);
C = hadamard(4) / 2;

U = S * kron(I, C); % Ajjaj ezek itt sorok lettek, nem oszlopok!

start = kron(start_pos, start_coin);

result = (U^100*start')'

prob = zeros(1,N);
for k=1:N
  posn = zeros(1,N);
  posn(1,k) = 1;
  M_hat_k = kron(posn'*posn, eye(4));
  proj = M_hat_k * result';
  prob(1,k) = proj'*conj(proj);
end

function ret = step2d(i, stepx, stepy, n)
  i_x = mod(i,n);
  i_y = floor(i/n);
  
  ret_x = mod(i_x+stepx, n);
  ret_y = mod(i_y+stepy, n);
  ret = ret_y * n + ret_x;
end