"""
:module: JGLAC_Fig02_Steady_State_Parameter_Space.py
:purpose: Plot the modeled parameter space (N,\\tau,S,\\mu) for the UW-CRSD
		  assuming rheologic properties identical to those in Zoet & Iverson
		  (2015)
:version: 0 - Submission format to Journal of Glaciology
:short ref: Stevens, Hansen, and others
			Experimental constraints on transient glacier sliding with ice-bed separation
:Figure #: 2
:Figure Caption: Parameter space for the double-valued drag sliding model of Zoet and Iverson (2015) 
				 for the geometry of the UW¬–CRSD and the sinusoidal bed in this study (Table 1) and 
				 UW–CRSD operational limits (Table 2). 
				 	Figure axes show linear slip velocities, V, and effective pressures, N. 
				 	Shading shows predicted \\mu (colorbar) 
				 	solid contours show predicted shear stresses, \tau, and 
				 	dotted contours represent predicted the ice-bed contact area fractions, S. 
				 	The operational limit \tau_{max} = 275 kPa is shown as a red dashed line. 
				 	The operational range of N(t) for these experiments are shown as an orange
				 	line on the centerline velocity, V = 15 m a^{-1} and surrounded by an orange
				 	shaded region that bounds the inner and outer diameter velocities V\\in[X, Y]
:auth: Nathan T. Stevens
:email: ntstevens@wisc.edu

TODO: Cleanup help documentation
"""
import os, argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main(args):
	path = args.input_path
	# path = os.path.join('..','results','model')
	df_N = pd.read_csv(os.path.join(path,'SigmaN_kPa_grid.csv'), index_col=[0])
	df_U = pd.read_csv(os.path.join(path,'Slip_mpy_grid.csv'), index_col=[0])
	df_S = pd.read_csv(os.path.join(path,'S_total_grid.csv'), index_col=[0])
	df_T = pd.read_csv(os.path.join(path,'Tau_kPa_grid.csv'), index_col=[0])
	# Calculate Drag
	df_u = df_T/df_N
	df_u[~np.isfinite(df_u.values)] = np.nan


	fig = plt.figure(figsize=(6,4.5))
	pch = plt.pcolor(df_U.values, df_N.values, df_u.values, cmap='Blues')
	plt.colorbar(pch)
	plt.text(38,500,'Drag ($\\mu$) [ - ]',rotation=270,fontsize=10,ha='center',va='center')
	plt.clim([0,.35])

	# Shear stress contours
	ch = plt.contour(df_U.values, df_N.values, df_T.values,
					levels=np.arange(25,275,25), colors=['k'])
	chm = plt.contour(df_U.values, df_N.values, df_T.values,
					levels=[275], colors=['r'], linestyles='--')

	chS = plt.contour(df_U.values, df_N.values, df_S.values,
					levels=np.arange(0.1,1,0.1), colors=['w'], linestyles=':')


	# Plot operational range for N(t)
	plt.plot([15]*2,[210,490],linewidth=4,color='orange',zorder=9,alpha=1)
	plt.plot(15,350,'d',color='orange',markersize=14,alpha=1)
	## This isn't quite right because the bed is kambered. Leave out for now
	# plt.fill_between([7.5,22.5],[210]*2,[490]*2,color='orange',alpha=0.5,zorder=8)
	plt.text(0.25,800,'No Cavities\n($S$ = 1)',fontsize=10,va='center')

	# Plot V < V_{min} zone
	plt.fill_between([0,4],[100]*2,[900]*2,color='black',alpha=0.1)

	# Axis Labels
	plt.xlabel('Linear Sliding Velocity [$V$] ($m$ $a^{-1}$)')
	plt.ylabel('Effective Pressure [$N$] (kPa)')
	plt.xlim([0, 30])

	# Plot shear stress contour labels
	mlocs = []; cxloc = 23
	# Custom contour label positions
	for level in ch.collections:
		path = level.get_paths()
		if len(path) > 0:
			cxpath = path[0].vertices[:,0]
			cypath = path[0].vertices[:,1]
			cxidx = np.argmin(np.abs(cxpath - cxloc))
			cyloc = cypath[cxidx]
			mlocs.append((cxloc,cyloc))
			# mlocs.append((np.mean(level.get_paths()[0].vertices[:,0]),\
			# 	 		  np.mean(level.get_paths()[0].vertices[:,1])))
	plt.clabel(ch,inline=True,inline_spacing=2,fontsize=10,fmt='%d kPa',manual=mlocs)

	mlocs = []
	for level in chm.collections:
		path = level.get_paths()
		if len(path) > 0:
			cxpath = path[0].vertices[:,0]
			cypath = path[0].vertices[:,1]
			cxidx = np.argmin(np.abs(cxpath - cxloc))
			cyloc = cypath[cxidx]
			mlocs.append((cxloc,cyloc))
			# mlocs.append((np.mean(level.get_paths()[0].vertices[:,0]),\
			# 	 		  np.mean(level.get_paths()[0].vertices[:,1])))
	plt.clabel(chm,inline=True,inline_spacing=2,fontsize=10,fmt='%d kPa',manual=mlocs)

	mlocs = []; cxloc = 9
	for level in chS.collections:
		path = level.get_paths()
		if len(path) > 0:
			cxpath = path[0].vertices[:,0]
			cypath = path[0].vertices[:,1]
			cxidx = np.argmin(np.abs(cxpath - cxloc))
			cyloc = cypath[cxidx]
			mlocs.append((cxloc,cyloc))
			# mlocs.append((np.mean(path[0].vertices[:,0]),\
			# 	 		  np.mean(path[0].vertices[:,1])))

	plt.clabel(chS,inline=True,inline_spacing=2,fontsize=10,fmt='%.1f',manual=mlocs)

	if not args.render_only:
		if args.dpi == 'figure':
			dpi = 'figure'
		else:
			try:
				dpi = int(args.dpi)

			except:
				dpi = 'figure'
		if dpi == 'figure':
			savename = os.path.join(args.output_path, f'JGLAC_Fig02_fdpi.{args.format}')
		else:
			savename = os.path.join(args.output_path, f'JGLAC_Fig02_{dpi}dpi.{args.format}')
		if not os.path.exists(os.path.split(savename)[0]):
			os.makedirs(os.path.split(savename)[0])
		plt.savefig(savename, dpi=dpi, format=args.format)

	if args.show:
		plt.show()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		prog='Figure_02 : Steady State Theory Parameter Space'
	)


	parser = argparse.ArgumentParser(
		prog='JGLAC_Fig02.py',
		description='A steady state parameter space for the Lliboutry/Kamb sliding law for ice over an undulatory bed'
	)

	parser.add_argument(
		'-i',
		'--input_path',
		dest='input_path',
		default=os.path.join('.','processed_data','steadystate'),
		help='Path to pandas *grid.csv files generated by src/primary/generate_parameter_space.py',
		type=str
	)
	

	parser.add_argument(
		'-o',
		'--output_path',
		action='store',
		dest='output_path',
		default=os.path.join('..','results','figures'),
		help='path and name to save the rendered figure to, minus format (use -f for format). Defaults to "../results/figures/JGLAC_Fig01c"',
		type=str
	)

	parser.add_argument(
		'-f',
		'-format',
		action='store',
		dest='format',
		default='png',
		choices=['png','pdf','svg'],
		help='the figure output format (e.g., *.png, *.pdf, *.svg) callable by :meth:`~matplotlib.pyplot.savefig`. Defaults to "png"',
		type=str
	)

	parser.add_argument(
		'-d',
		'--dpi',
		action='store',
		dest='dpi',
		default='figure',
		help='set the `dpi` argument for :meth:`~matplotlib.pyplot.savefig. Defaults to "figure"'
	)

	parser.add_argument(
		'-s',
		'--show',
		action='store_true',
		dest='show',
		help='if included, render the figure on the desktop in addition to saving to disk'
	)

	parser.add_argument(
		'-r',
		'--render_only',
		dest='render_only',
		action='store_true',
		help='including this flag skips saving to disk'
	)

	args = parser.parse_args()
	main(args)