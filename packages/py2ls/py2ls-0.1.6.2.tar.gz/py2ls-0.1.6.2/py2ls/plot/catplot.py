import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba
from scipy.stats import gaussian_kde

def catplot(data, *args, **kwargs):
    """
    catplot(data, opt=None, ax=None)

    Args:
        data (array): data matrix
    """
    def plot_bars(data_m, opt_b, xloc, ax):
        bar_positions = get_positions(xloc, opt_b['loc'], opt_b['x_width'], data.shape[0])
        bar_positions=np.nanmean(bar_positions,axis=0)
        for i, (x, y) in enumerate(zip(bar_positions, data_m)):
            color = to_rgba(opt_b['FaceColor'][i % len(opt_b['FaceColor'])])
            ax.bar(x, y, 
                    width=opt_b['x_width'], 
                    color=color,
                    edgecolor=opt_b['EdgeColor'], 
                    alpha=opt_b['FaceAlpha'])

    def plot_errors(data, data_m, opt_e, xloc, ax):
        error_positions = get_positions(xloc, opt_e['loc'], opt_e['x_width'], data.shape[0])
        error_positions=np.nanmean(error_positions,axis=0)
        errors = np.nanstd(data, axis=0)
        if opt_e['error'] == 'sem':
            errors /= np.sqrt(np.sum(~np.isnan(data),axis=0))

        if not isinstance(opt_e['FaceColor'],list):
            opt_e['FaceColor']=[opt_e['FaceColor']]
        if not isinstance(opt_e['MarkerEdgeColor'],list):
            opt_e['MarkerEdgeColor']=[opt_e['MarkerEdgeColor']]  
        for i, (x, y, err) in enumerate(zip(error_positions, data_m, errors)):
            ax.errorbar(x, y, yerr=err, 
                        fmt=opt_e['Marker'], 
                        ecolor=opt_e['LineColor'], 
                        elinewidth=opt_e['LineWidth'], 
                        lw=opt_e['LineWidth'], 
                        ls=opt_e['LineStyle'], 
                        capsize=opt_e['CapSize'],
                        capthick=opt_e['CapLineWidth'], 
                        markersize=opt_e['MarkerSize'],
                        mec=opt_e['MarkerEdgeColor'][i % len(opt_e['MarkerEdgeColor'])],
                        mfc=opt_e['FaceColor'][i % len(opt_e['FaceColor'])],
                        visible=opt_e['Visible']
                        )

    def plot_scatter(data, opt_s, xloc, ax):
        scatter_positions = get_positions(xloc, opt_s['loc'], opt_s['x_width'], data.shape[0])
        for i, (x, y) in enumerate(zip(scatter_positions.T, data.T)):
            color = to_rgba(opt_s['FaceColor'][i % len(opt_s['FaceColor'])])
            ax.scatter(x, y, 
                        color=color, 
                        alpha=opt_s['FaceAlpha'], 
                        edgecolor=opt_s['MarkerEdgeColor'], 
                        s=opt_s['MarkerSize'],
                        marker=opt_s['Marker']
                        )

    def plot_boxplot(data, bx_opt, xloc,ax):
        if 'l' in bx_opt['loc']:
            X_bx = xloc - bx_opt['x_width']
        elif 'r' in bx_opt['loc']:
            X_bx = xloc + bx_opt['x_width']
        elif 'i' in bx_opt['loc']:
            X_bx = xloc
            X_bx[:, 0] += bx_opt['x_width']
            X_bx[:, -1] -= bx_opt['x_width']
        elif 'o' in bx_opt['loc']:
            X_bx = xloc
            X_bx[:, 0] -= bx_opt['x_width']
            X_bx[:, -1] += bx_opt['x_width']
        elif 'c' in bx_opt['loc'] or 'm' in bx_opt['loc']:
            X_bx = xloc
        else:
            X_bx = xloc
 

        boxprops = dict(color=bx_opt['EdgeColor'], 
                        linewidth=bx_opt['BoxLineWidth'])
        flierprops = dict(marker=bx_opt['OutlierMarker'], 
                        markerfacecolor=bx_opt['OutlierColor'],
                        markersize=bx_opt['OutlierSize'])
        whiskerprops = dict(linestyle=bx_opt['WhiskerLineStyle'], 
                            color=bx_opt['WhiskerLineColor'], 
                            linewidth=bx_opt['WhiskerLineWidth'])
        capprops = dict(color=bx_opt['CapLineColor'], 
                        linewidth=bx_opt['CapLineWidth'],)
        medianprops = dict(linestyle=bx_opt['MedianLineStyle'], 
                        color=bx_opt['MedianLineColor'], 
                        linewidth=bx_opt['MedianLineWidth'])
        meanprops = dict(linestyle=bx_opt['MeanLineStyle'], 
                color=bx_opt['MeanLineColor'], 
                linewidth=bx_opt['MeanLineWidth'])
        bxp = ax.boxplot(data, 
                        positions=X_bx, 
                        notch=bx_opt['Notch'], 
                        patch_artist=True, 
                        boxprops=boxprops, 
                        flierprops=flierprops, 
                        whiskerprops=whiskerprops, 
                        capwidths=bx_opt['CapSize'],
                        showfliers = bx_opt['Outliers'],
                        showcaps = bx_opt['Caps'],
                        capprops=capprops, 
                        medianprops=medianprops, 
                        meanline=bx_opt['MeanLine'],
                        showmeans=bx_opt['MeanLine'],
                        meanprops =meanprops,
                        widths=bx_opt['x_width'])

        if bx_opt['BoxLineWidth'] < 0.1:
            bx_opt['EdgeColor'] = 'none'
        else:
            bx_opt['EdgeColor'] = bx_opt['EdgeColor']

        for patch, color in zip(bxp['boxes'], bx_opt['FaceColor']):
            patch.set_facecolor(to_rgba(color, bx_opt['FaceAlpha']))

        if bx_opt['MedianLineTop']:
            ax.set_children(ax.get_children()[::-1])  # move median line forward

    def plot_violin(data, opt_v, xloc, ax):
        violin_positions = get_positions(xloc, opt_v['loc'], opt_v['x_width'], data.shape[0])
        violin_positions = np.nanmean(violin_positions, axis=0)
        for i, (x, ys) in enumerate(zip(violin_positions, data.T)):
            ys = ys[~np.isnan(ys)]
            if len(ys) > 1:
                kde = gaussian_kde(ys, bw_method=opt_v['BandWidth'])
                min_val, max_val = ys.min(), ys.max()
                y_vals = np.linspace(min_val, max_val, opt_v['NumPoints'])
                kde_vals = kde(y_vals)
                kde_vals = kde_vals / kde_vals.max() * opt_v['x_width']
                if 'r' in opt_v['loc'].lower():
                    ax.fill_betweenx(y_vals, x, x + kde_vals,
                                    color=opt_v['FaceColor'][i % len(opt_v['FaceColor'])], 
                                    alpha=opt_v['FaceAlpha'],
                                    edgecolor=opt_v['EdgeColor'])
                elif 'l' in opt_v['loc'].lower() and not 'f' in opt_v['loc'].lower() :
                    ax.fill_betweenx(y_vals, x - kde_vals, x,
                                    color=opt_v['FaceColor'][i % len(opt_v['FaceColor'])], 
                                    alpha=opt_v['FaceAlpha'],
                                    edgecolor=opt_v['EdgeColor'])
                elif 'o' in opt_v['loc'].lower() or 'both' in opt_v['loc'].lower() :
                    ax.fill_betweenx(y_vals, x - kde_vals, x + kde_vals,
                                    color=opt_v['FaceColor'][i % len(opt_v['FaceColor'])], 
                                    alpha=opt_v['FaceAlpha'],
                                    edgecolor=opt_v['EdgeColor'])
                elif 'i' in opt_v['loc'].lower():
                    if i % 2 == 1:  # odd number
                        ax.fill_betweenx(y_vals, x -kde_vals, x,
                                        color=opt_v['FaceColor'][i % len(opt_v['FaceColor'])], 
                                        alpha=opt_v['FaceAlpha'],
                                        edgecolor=opt_v['EdgeColor'])
                    else:
                        ax.fill_betweenx(y_vals, x, x+kde_vals,
                                        color=opt_v['FaceColor'][i % len(opt_v['FaceColor'])], 
                                        alpha=opt_v['FaceAlpha'],
                                        edgecolor=opt_v['EdgeColor'])
                elif 'f' in opt_v['loc'].lower():
                    ax.fill_betweenx(y_vals, x - kde_vals, x + kde_vals,
                                    color=opt_v['FaceColor'][i % len(opt_v['FaceColor'])], 
                                    alpha=opt_v['FaceAlpha'],
                                    edgecolor=opt_v['EdgeColor'])
                    
    def plot_lines(data, opt_l, opt_s, ax): 
        scatter_positions = get_positions(xloc, opt_s['loc'], opt_s['x_width'], data.shape[0])
        for incol in range(data.shape[1]-1):
            for irow in range(data.shape[0]):
                if not np.isnan(data[irow, incol]):
                    if opt_l['LineStyle'] is not None and not opt_l['LineStyle'] =='none':
                        x_data = [scatter_positions[irow, incol], scatter_positions[irow, incol + 1]]
                        y_data = [data[irow, incol], data[irow, incol + 1]]
            

                        ax.plot(x_data, y_data,
                                color=opt_l['LineColor'],
                                linestyle=opt_l['LineStyle'],
                                linewidth=opt_l['LineWidth'],
                                alpha=opt_l['LineAlpha'])
                            
    def get_positions(xloc, loc_type, x_width, n_row=None):
        if 'rand' in loc_type:
            scatter_positions = np.zeros((n_row, len(xloc)))
            np.random.seed(111)
            for i, x in enumerate(xloc):
                scatter_positions[:, i] = np.random.uniform(x - x_width, x + x_width, n_row)
            return scatter_positions
        elif 'l' in loc_type:
            return np.tile(xloc - x_width,(n_row,1))
        elif 'r' in loc_type and not 'd' in loc_type:
            return np.tile(xloc + x_width,(n_row,1))
        elif 'i' in loc_type:
            return np.tile(np.concatenate([xloc[:1] + x_width, xloc[1:-1], xloc[-1:] - x_width]),(n_row,1))
        elif 'o' in loc_type:
            return np.tile(np.concatenate([xloc[:1] - x_width, xloc[1:-1], xloc[-1:] + x_width]),(n_row,1))
        else:
            return np.tile(xloc,(n_row,1))
    
    opt = kwargs.get('opt',{}) 
    ax = kwargs.get('ax',None)
    if 'ax' not in locals() or ax is None:
        ax=plt.gca()

    default_colors = np.array([
        [0, 0, 0],
        [234, 37, 46],
        [0, 154, 222],
        [175, 89, 186],
        [255, 198, 37],
        [242, 133, 34]
    ]) / 255.0

    opt.setdefault('c', default_colors)
    if len(opt['c']) < data.shape[1]:
        additional_colors = plt.cm.winter(np.linspace(0, 1, data.shape[1] - len(opt['c'])))
        opt['c'] = np.vstack([opt['c'], additional_colors[:, :3]])

    opt.setdefault('loc', {})
    opt['loc'].setdefault('go', 0)
    opt['loc'].setdefault('xloc', np.arange(1, data.shape[1] + 1))

    # export setting
    opt.setdefault('export', False)
    opt['export'].setdefault('path', None)
    print(opt['export'])

    opt.setdefault('b', {})
    opt['b'].setdefault('go', 0) 
    opt['b'].setdefault('EdgeColor', 'k')
    opt['b'].setdefault('FaceAlpha', 1)
    opt['b'].setdefault('EdgeAlpha', 1)
    opt['b'].setdefault('LineStyle', '-')
    opt['b'].setdefault('x_width', 0.5)
    opt['b'].setdefault('ShowBaseLine', 'off')
    opt['b'].setdefault('loc', 'c')
    opt['b'].setdefault('FaceColor', opt['c'])

    opt.setdefault('e', {})
    opt['e'].setdefault('go', 1) 
    opt['e'].setdefault('LineWidth', 1)
    opt['e'].setdefault('CapLineWidth', 1)
    opt['e'].setdefault('CapSize', opt['b']['x_width'] * 100 * 0.1)
    opt['e'].setdefault('Marker', 'none')
    opt['e'].setdefault('LineStyle', 'none')
    opt['e'].setdefault('LineColor', 'k')
    opt['e'].setdefault('LineJoin', 'round')
    opt['e'].setdefault('MarkerSize', 'auto')
    opt['e'].setdefault('FaceColor', opt['c'])
    opt['e'].setdefault('MarkerEdgeColor', 'none')
    opt['e'].setdefault('Visible', True)
    opt['e'].setdefault('Orientation', 'vertical')
    opt['e'].setdefault('error', 'sem')
    opt['e'].setdefault('loc', 'c')
    opt['e'].setdefault('x_width', opt['b']['x_width'] / 5)
    opt['e'].setdefault('cap_dir', 'b')

    opt.setdefault('s', {})
    opt['s'].setdefault('go', 1) 
    opt['s'].setdefault('x_width', opt['b']['x_width'] / 5)
    opt['s'].setdefault('Marker', 'o')
    opt['s'].setdefault('MarkerSize', 6)  # Set default size for markers
    opt['s'].setdefault('LineWidth', 1)
    opt['s'].setdefault('FaceColor', opt['c'])
    opt['s'].setdefault('FaceAlpha', 0.6)
    opt['s'].setdefault('loc', 'random')
    opt['s'].setdefault('MarkerEdgeColor', None)

    opt.setdefault('bx', {})
    opt['bx'].setdefault('go', 0)
    opt['bx'].setdefault('EdgeColor', 'k')
    opt['bx'].setdefault('FaceAlpha', 1)
    opt['bx'].setdefault('EdgeAlpha', 1)
    opt['bx'].setdefault('LineStyle', '-')
    opt['bx'].setdefault('x_width', 0.5)
    opt['bx'].setdefault('ShowBaseLine', 'off')
    opt['bx'].setdefault('loc', 'c')
    opt['bx'].setdefault('FaceColor', opt['c'])
    opt['bx'].setdefault('Notch', False)
    opt['bx'].setdefault('MedianStyle', 'line')
    opt['bx'].setdefault('Outliers', 'on')
    opt['bx'].setdefault('OutlierMarker', '+')
    opt['bx'].setdefault('OutlierColor', 'r')
    opt['bx'].setdefault('OutlierSize', 6)
    opt['bx'].setdefault('PlotStyle', 'traditional')
    opt['bx'].setdefault('FactorDirection', 'auto')
    opt['bx'].setdefault('Whisker', 1.5)
    opt['bx'].setdefault('Orientation', 'vertical')
    opt['bx'].setdefault('BoxLineWidth', 1.5)
    opt['bx'].setdefault('FaceColor', 'k')
    opt['bx'].setdefault('WhiskerLineStyle', '-')
    opt['bx'].setdefault('WhiskerLineColor', 'k')
    opt['bx'].setdefault('WhiskerLineWidth', 1.5)
    opt['bx'].setdefault('Caps', True)
    opt['bx'].setdefault('CapLineColor', 'k')
    opt['bx'].setdefault('CapLineWidth', 1.5)
    opt['bx'].setdefault('CapSize', 0.35)
    opt['bx'].setdefault('MedianLineStyle', '-')
    opt['bx'].setdefault('MedianLineColor', 'k')
    opt['bx'].setdefault('MedianLineWidth', 1.5)
    opt['bx'].setdefault('MedianLineTop', False)
    opt['bx'].setdefault('MeanLine', False)
    opt['bx'].setdefault('showmeans', opt['bx']['MeanLine'])
    opt['bx'].setdefault('MeanLineStyle', '-')
    opt['bx'].setdefault('MeanLineColor', 'b')
    opt['bx'].setdefault('MeanLineWidth', 1.5)
    
    # Violin plot options
    opt.setdefault('v', {})
    opt['v'].setdefault('go', 1)
    opt['v'].setdefault('x_width', 0.3)
    opt['v'].setdefault('loc', 'r')
    opt['v'].setdefault('EdgeColor', 'none')
    opt['v'].setdefault('FaceColor', opt['c'])
    opt['v'].setdefault('FaceAlpha', 0.3)
    opt['v'].setdefault('BandWidth', 'scott')
    opt['v'].setdefault('Function', 'pdf')
    opt['v'].setdefault('Kernel', 'gau')
    opt['v'].setdefault('NumPoints', 500)
    opt['v'].setdefault('BoundaryCorrection', 'reflection')
    
    # line plot options
    opt.setdefault('l', {})
    opt['l'].setdefault('go', 0)
    opt['l'].setdefault('LineStyle', '-')
    opt['l'].setdefault('LineColor', 'k')
    opt['l'].setdefault('LineWidth', 0.5)
    opt['l'].setdefault('LineAlpha', 0.5) 

    data_m = np.nanmean(data, axis=0)
    nr, nc = data.shape

    xloc = opt['loc']['xloc']

    if opt['b']['go']:
        plot_bars(data_m, opt['b'], xloc, ax)

    if opt['e']['go']:
        plot_errors(data, data_m, opt['e'], xloc, ax)

    if opt['s']['go']:
        plot_scatter(data, opt['s'], xloc, ax)
        
    if opt['bx']['go']:
        plot_boxplot(data, opt['bx'], xloc, ax)
    if opt['v']['go']:
        plot_violin(data, opt['v'], xloc, ax) 
    if opt['l']['go'] and opt['s']['go']:
        plot_lines(data, opt['l'], opt['s'], ax)

    return ax

# from py2ls.ips import get_color,figsets
# opt={}
# opt = {
#     'export':{'path':get_cwd()},
#     'c': get_color(5,cmap='jet',by='linspace'),  # Custom colors for 3 categories
#     'b': {
#         'go': 0,  
#         'x_width': 0.85,
#         'FaceAlpha': 0.7,
#         'EdgeColor':'none'
#     },
#     'e': {
#         'loc':'r',
#         'go': 1,
#         'error': 'sem',
#         'Marker':'d',
#         'CapSize': 1,
#         'LineWidth':1,
#         'CapLineWidth':8,
#         'LineStyle':'--',
#         'MarkerSize':6,
#         'LineColor':'k',
#         'FaceColor':get_color(10),
#         'MarkerEdgeColor':'none',
#         'Visible':True
#     },
#     's': {
#         'go': 1,
#         'x_width':0.2,
#         'loc':'random',
#         'Marker': 'o',
#         # 'MarkerSize': 20,
#         'FaceAlpha': 1,
#         'FaceColor':'k',
#         'LineWidth':1
        
#     },
#     'bx':{
#         'go':1,
#         'FaceAlpha':0.8,
#         'EdgeColor':'none',
#         'loc':'c',
#         'x_width':0.2,
#         'WhiskerLineWidth':1,
#         'MedianLineWidth':2,
#         # 'MedianLineColor':'r',
#         'OutlierMarker':'+',
#         'OutlierColor':'r',
#         'CapSize':.2,
#         # 'Caps':False,
#         # 'CapLineColor':'r',
#         # 'CapLineWidth':8,
#         # 'MeanLine':True,
#         # 'FaceColor':['r','g','b','m','c']
#         },
#     'v':{
#         'go':0,
#         'loc':'r',
#         'x_width':0.2,
#         'FaceAlpha':0.51,
#          },
#     'l':{
#         'go':1,
#         'LineColor':'k'
#         }
# }
# data1 = np.random.rand(10, 5)
# data2 = np.random.rand(10, 5)
# fig, axs=plt.subplots(1,2,figsize=(6,2.5))
# catplot(data1, opt=opt,ax=axs[0])
# catplot(data2, opt=opt,ax=axs[1])
# figsets(sp=5,
#         ax=axs[0],
#         xticks=np.arange(1,6,1),
#         xtickslabel=['glua1','glua2','a','b','c'],
#         xlabel='proteins',
#         xangle=90,
#         yticks=np.arange(0,2,0.5),
#         xlim=[0.75, 5.1],
#         ticks=dict(pad=1,c='k'))

# figsave("/Users/macjianfeng/Dropbox/Downloads/",'test.pdf')

