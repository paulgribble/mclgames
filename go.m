% go.m
% analyses output from goarm5.py

load out1.asc
time = out1(:,1);
score = out1(:,2);
tgthit = out1(:,3);
tgtn = out1(:,4);
tx = out1(:,5);
ty = out1(:,6);
hx = out1(:,7);
hy = out1(:,8);
qs = out1(:,9);
qe = out1(:,10);
qsd = out1(:,11);
qed = out1(:,12);
qsdd = out1(:,13);
qedd = out1(:,14);
sf = out1(:,15);
se = out1(:,16);
ef = out1(:,17);
ee = out1(:,18);
ksf = out1(:,19);
kse = out1(:,20);
kef = out1(:,21);
kee = out1(:,22);

% beginning of each trial
itrial = [1; find(tgthit==1); size(out1,1)];

n = length(itrial)-1; % number of trials
Msf = zeros(n,1);
Mse = zeros(n,1);
Mef = zeros(n,1);
Mee = zeros(n,1);
Tgt = zeros(n,1);
for i=1:n
    Msf(i) = sum(sf(itrial(i):itrial(i+1)));
    Mse(i) = sum(se(itrial(i):itrial(i+1)));
    Mef(i) = sum(ef(itrial(i):itrial(i+1)));
    Mee(i) = sum(ee(itrial(i):itrial(i+1)));
    Tgt(i) = tgtn(itrial(i));
end

