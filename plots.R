library('ggplot2')

df = rbind( read.csv('pypy-results.txt', sep='\t'), read.csv('cpy-results.txt', sep='\t') )
df = subset(df, rep==2)




ggplot(subset(df, host!='paste') , aes(x=conc, y=reqs_per_sec, colour=name, line=pypy)) 
last_plot() + geom_line() + facet_wrap(~host) + xlim(0,256) + xlab('Concurrent requests') + ylab('Requests per second')
ggsave('rqs.png')

df$reqs_per_sec = NULL

dfm = melt(df, id.vars=c('pypy', 'name', 'host', 'conc', 'rep'))
dfm = subset(dfm, variable!='reqs_per_sec')


ggplot(dfm, aes(x=conc, y=value, colour=variable, line=pypy)) + geom_line() + facet_wrap(name~host) + ylim(0,10000) + scale_x_log2() + scale_y_log2()
ggsave('time.png')


