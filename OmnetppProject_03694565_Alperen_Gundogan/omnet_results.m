%% Task 2.3.3 - Channel Utilization fullLoad

figure(1);
clf;
fullLoad = 0.1:0.1:1;
ch_uti =  [0.0914901	0.167032	0.216453	0.272463	0.296884	0.32248	0.345446	0.357442	0.371405	0.383078];
plot(fullLoad, ch_uti, 'b','LineWidth',2, 'MarkerSize', 10);
grid on;
title("Task 2.3.3");
xlabel("Full Load");
ylabel("Channel Utilization");

%% Task 3.1.6
%% maxReTx = 0
figure(2);
clf;
fullLoad = 0.1:0.1:1;
ch_uti_1 = [0.091563352666134995 0.167166173373290011 0.216626577330120001 0.272681701814529998 0.297121608091339973 0.322738527377289974 0.345723227657870003 0.357728425673690009 0.371702429736209983 0.383384923132379984];
plot(fullLoad, ch_uti_1,'r', 'LineWidth',2, 'MarkerSize', 10);
grid on;
title("Task 3.1.6");
xlabel("Full Load");
ylabel("Channel Utilization");
 
%% Task 4.1.2
%% fullLoad = 0.4, maxReTx = 4
figure(3);
clf;
maxBackOff = 1:1:20;
ch_uti_2 = [0.305698	0.310352	0.294964	0.311344	0.294353	0.310207	0.318877	0.295264	0.293994	0.292766	0.293295	0.297741	0.299061	0.302849	0.308046	0.295552	0.29943	0.29989	0.291096	0.31];
plot(maxBackOff, ch_uti_2, 'g', 'LineWidth',2, 'MarkerSize', 10);
grid on;
legend show
title("Task 4.1.2");
xlabel("Maximum Backoff");
ylabel("Channel Utilization");



