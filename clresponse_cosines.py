from classy import Class
import matplotlib.pyplot as plt
import numpy as np


params = {
	    'output': 'tCl lCl',
	    'l_max_scalars': 2508,
	    'lensing': 'yes',
	    'P_k_ini type': 'external_Pk',
	    'command': 'python /home/andrew/Research/tools/class_public-2.4.3/external_Pk/generate_Pk_cosines.py',
	    'custom1': 0,
	    'custom2': 0,
	    'custom3': 0,
	    'custom4': 0,
	    'custom5': 0}

#Get the unperturbed cls for comparison
cosmo = Class()
cosmo.set(params)
cosmo.compute()
clso=cosmo.lensed_cl(2508)['tt'][30:]
ell = cosmo.lensed_cl(2508)['ell'][30:]

for i in range(len(clso)):
	clso[i]=ell[i]*(ell[i]+1)/(4*np.pi)*((2.726e6)**2)*clso[i]
a=np.zeros(5)
cosmo.struct_cleanup()
cosmo.empty()
dcls=np.zeros([clso.shape[0],5])
h=1e-6
for m in range(5):
	a[m]=h
	# Define your cosmology (what is not specified will be set to CLASS default parameters)
	params = {
	    'output': 'tCl lCl',
	    'l_max_scalars': 2508,
	    'lensing': 'yes',
	    'P_k_ini type': 'external_Pk',
	    'command': 'python /home/andrew/Research/tools/class_public-2.4.3/external_Pk/generate_Pk_cosines.py',
	    'custom1': a[0],
	    'custom2': a[1],
	    'custom3': a[2],
	    'custom4': a[3],
	    'custom5': a[4]}

	# Create an instance of the CLASS wrapper
	cosmo = Class()
	# Set the parameters to the cosmological code
	cosmo.set(params)
	# Run the whole code. Depending on your output, it will call the
	# CLASS modules more or less fast. For instance, without any
	# output asked, CLASS will only compute background quantities,
	# thus running almost instantaneously.
	# This is equivalent to the beginning of the `main` routine of CLASS,
	# with all the struct_init() methods called.
	cosmo.compute()
	# Access the lensed cl until l=2000
	cls = cosmo.lensed_cl(2508)['tt'][30:]
	ell = cosmo.lensed_cl(2508)['ell'][30:]

	for i in range(len(cls)):
		cls[i]=ell[i]*(ell[i]+1)/(4*np.pi)*((2.726e6)**2)*cls[i]
	dcls[:,m]=(cls-clso)/h


	# Clean CLASS (the equivalent of the struct_free() in the `main`
	# of CLASS. This step is primordial when running in a loop over different
	# cosmologies, as you will saturate your memory very fast if you ommit
	# it.
	cosmo.struct_cleanup()
	a[m]=0
# If you want to change completely the cosmology, you should also
# clean the arguments, otherwise, if you are simply running on a loop
# of different values for the same parameters, this step is not needed
cosmo.empty()

#dcls=responses[amps[max_index-1]][1:,0:]
np.savetxt('xmat_cosines.txt',dcls, fmt='%1.4e')
#np.savetxt('pert_size.txt',[amps[max_index-1]*2.41e-9,amps[max_index]*2.41e-9], fmt='%1.4e')
