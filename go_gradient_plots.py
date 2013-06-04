def goplot(fname):
    d = genfromtxt("%s.log" % (fname))
    figure()
    subplot(2,1,1)
    plot(d[:,3], 'r-')
    plot(d[:,5], 'b.-')
    ylabel('X DEV (pixels)')
    title(fname)
    subplot(2,1,2)
    plot(d[:,4], 'r-')
    plot(d[:,6], 'b.-')
    ylabel('TIMING (sec)')
    xlabel('TIME (trial)')

