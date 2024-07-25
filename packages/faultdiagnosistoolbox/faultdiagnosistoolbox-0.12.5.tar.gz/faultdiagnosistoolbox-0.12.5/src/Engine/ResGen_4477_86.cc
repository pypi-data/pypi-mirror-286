#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/ndarrayobject.h>

#ifdef _WIN32
#define _USE_MATH_DEFINES
#include <cmath>
#endif

#include "extmodelfuns.h"

// RESGEN_4477_86 Sequential residual generator for model 'VEP4'
// Causality: int
//
// Structurally sensitive to faults: fp_af, fw_af, fw_th, fw_c, fc_vol, fw_t, fx_th, fyT_ic
//
// Example of basic usage:
// Let z be the observations matrix, each column corresponding to a known signal and Ts the sampling time,
// then the residual generator can be simulated by:
//
// state = {'wg_pos': wg_pos_0, 'T_im': T_im_0, 'm_af': m_af_0, 'T_af': T_af_0, 'm_c': m_c_0, 'T_c': T_c_0, 'm_ic': m_ic_0, 'T_ic': T_ic_0, 'm_im': m_im_0, 'm_em': m_em_0, 'T_em': T_em_0, 'm_t': m_t_0, 'T_t': T_t_0, 'omega_tc': omega_tc_0}
// r = ResGen_4477_86( z, state, params, Ts )
//
// State is a dictionary with the keys: wg_pos, T_im, m_af, T_af, m_c, T_c, m_ic, T_ic, m_im, m_em, T_em, m_t, T_t, omega_tc

// File generated Thu Jul 18 15:25:22 2024

typedef struct {
  double H_af;
  double plin_af;
  double H_exhaust;
  double plin_exh;
  double H_intercooler;
  double plin_intercooler;
  double PIli_th;
  double gamma_air;
  double PIli_wg;
  double gamma_exh;
  double R_air;
  double cp_air;
  double V_af;
  double V_c;
  double V_ic;
  double V_im;
  double R_exh;
  double cp_exh;
  double lambda_af;
  double n_r;
  double r_c;
  double V_D;
  double CEva_cool;
  double D_c;
  double K1;
  double K2;
  double fix_gain;
  double eta_cmax;
  double eta_cmin;
  double T_std;
  double k1;
  double k2;
  double cp_eg;
  double gamma_eg;
  double tau_wg;
  double h_tot;
  double Amax;
  double A_0;
  double A_1;
  double A_2;
  double J_tc;
  double xi_fric_tc;
  double V_em;
  double V_t;
  double p_std;
  double a1;
  double a2;
  double a3;
  double a4;
  double a5;
  double Q_c11;
  double Q_c12;
  double Q_c22;
  double Cd;
  double PI_cmax;
  double cv_exh;
  double cv_air;
  double W_ccorrmax;
  double A_em;
  double K_t;
  double T0;
  double Cic_1;
  double Cic_2;
  double Cic_3;
  double TOL;
} Parameters;

typedef struct {
  double wg_pos;
  double T_im;
  double m_af;
  double T_af;
  double m_c;
  double T_c;
  double m_ic;
  double T_ic;
  double m_im;
  double m_em;
  double T_em;
  double m_t;
  double T_t;
  double omega_tc;
} ResState;

double ApproxInt(double dx, double x0, double Ts);
void GetParameters( PyObject *pyParams, Parameters* params );
void GetState( PyObject *pyStates, ResState* state );
void ResGen_4477_86_core( double* r, PyArrayObject *pyZ, npy_intp k, ResState *state, const Parameters *params, double Ts );

static PyObject*
ResGen_4477_86(PyObject *self, PyObject * args)
{
  PyArrayObject *pyZ;
  PyObject *pyState;
  PyObject *pyParams;
  double Ts;

  if (!PyArg_ParseTuple(args, "O!O!O!d", &PyArray_Type, &pyZ, &PyDict_Type, &pyState, &PyDict_Type, &pyParams, &Ts)) {
    return NULL;
  }

  if( PyArray_NDIM(pyZ) != 2 ) {
    return Py_BuildValue("");
  }
  npy_intp *shape = PyArray_SHAPE( pyZ );
  npy_intp N = shape[0];

  PyObject* pyR = PyArray_SimpleNew(1, &N, NPY_FLOAT64);
  double *r = (double *)PyArray_DATA((PyArrayObject *)pyR);


  ResState state;
  GetState(pyState, &state);

  Parameters params;
  GetParameters( pyParams, &params );

  // Main computational loop
  for( npy_intp k=0; k < N; k++ ) {
    ResGen_4477_86_core( &(r[k]), pyZ, k, &state, &params, Ts );
}

  return Py_BuildValue("O", pyR);
}

void
ResGen_4477_86_core(double* r, PyArrayObject *pyZ, npy_intp k, ResState* state, const Parameters *params, double Ts)
{
  // Parameters
  double H_af = params->H_af;
  double plin_af = params->plin_af;
  double H_exhaust = params->H_exhaust;
  double plin_exh = params->plin_exh;
  double H_intercooler = params->H_intercooler;
  double plin_intercooler = params->plin_intercooler;
  double PIli_th = params->PIli_th;
  double gamma_air = params->gamma_air;
  double PIli_wg = params->PIli_wg;
  double gamma_exh = params->gamma_exh;
  double R_air = params->R_air;
  double cp_air = params->cp_air;
  double V_af = params->V_af;
  double V_c = params->V_c;
  double V_ic = params->V_ic;
  double V_im = params->V_im;
  double R_exh = params->R_exh;
  double cp_exh = params->cp_exh;
  double lambda_af = params->lambda_af;
  double n_r = params->n_r;
  double r_c = params->r_c;
  double V_D = params->V_D;
  double CEva_cool = params->CEva_cool;
  double D_c = params->D_c;
  double K1 = params->K1;
  double K2 = params->K2;
  double fix_gain = params->fix_gain;
  double eta_cmax = params->eta_cmax;
  double eta_cmin = params->eta_cmin;
  double T_std = params->T_std;
  double k1 = params->k1;
  double k2 = params->k2;
  double cp_eg = params->cp_eg;
  double gamma_eg = params->gamma_eg;
  double tau_wg = params->tau_wg;
  double h_tot = params->h_tot;
  double Amax = params->Amax;
  double A_0 = params->A_0;
  double A_1 = params->A_1;
  double A_2 = params->A_2;
  double J_tc = params->J_tc;
  double xi_fric_tc = params->xi_fric_tc;
  double V_em = params->V_em;
  double V_t = params->V_t;
  double p_std = params->p_std;
  double a1 = params->a1;
  double a2 = params->a2;
  double a3 = params->a3;
  double a4 = params->a4;
  double a5 = params->a5;
  double Q_c11 = params->Q_c11;
  double Q_c12 = params->Q_c12;
  double Q_c22 = params->Q_c22;
  double Cd = params->Cd;
  double PI_cmax = params->PI_cmax;
  double cv_exh = params->cv_exh;
  double cv_air = params->cv_air;
  double W_ccorrmax = params->W_ccorrmax;
  double A_em = params->A_em;
  double K_t = params->K_t;
  double T0 = params->T0;
  double Cic_1 = params->Cic_1;
  double Cic_2 = params->Cic_2;
  double Cic_3 = params->Cic_3;
  double TOL = params->TOL;

  // Residual generator variables
  double W_af;
  double p_t;
  double W_es;
  double p_ic;
  double T_ic;
  double W_ic;
  double W_th;
  double Aeff_th;
  double W_wg;
  double Aeff_wg;
  double T_af;
  double p_af;
  double W_c;
  double T_cout;
  double T_c;
  double p_c;
  double T_imcr;
  double p_im;
  double T_im;
  double W_e;
  double T_ti;
  double T_em;
  double p_em;
  double dh_is;
  double W_twg;
  double T_turb;
  double T_t;
  double alpha_th;
  double omega_e;
  double Tq_c;
  double eta_c;
  double omega_tc;
  double PSI_c;
  double PI_c;
  double W_t;
  double Tq_t;
  double eta_t;
  double PI_t;
  double u_wg;
  double wg_pos;
  double T_e;
  double T_amb;
  double p_amb;
  double PSI_th;
  double PI_wg;
  double PSIli_wg;
  double m_af;
  double m_c;
  double m_ic;
  double T_fwd_flow_ic;
  double m_im;
  double m_em;
  double m_t;
  double PI_cnolim;
  double U_c;
  double PHI_model;
  double W_ccorr;
  double C_eta_vol;
  double T_in;
  double eta_vol;
  double W_ac;
  double W_fc;
  double T_tout;
  double Tflow_wg;
  double dmdt_af;
  double dTdt_af;
  double dmdt_c;
  double dTdt_c;
  double dmdt_ic;
  double dTdt_ic;
  double dmdt_im;
  double dTdt_im;
  double dmdt_em;
  double dTdt_em;
  double dmdt_t;
  double dTdt_t;
  double domegadt_tc;
  double dwgdt_pos;

  // Initialize state variables
  wg_pos = state->wg_pos;
  T_im = state->T_im;
  m_af = state->m_af;
  T_af = state->T_af;
  m_c = state->m_c;
  T_c = state->T_c;
  m_ic = state->m_ic;
  T_ic = state->T_ic;
  m_im = state->m_im;
  m_em = state->m_em;
  T_em = state->T_em;
  m_t = state->m_t;
  T_t = state->T_t;
  omega_tc = state->omega_tc;

  // Known signals
  double y_T_ic = *((double *)PyArray_GETPTR2(pyZ, k, 2));
  double y_omega_e = *((double *)PyArray_GETPTR2(pyZ, k, 4));
  double y_alpha_th = *((double *)PyArray_GETPTR2(pyZ, k, 5));
  double y_u_wg = *((double *)PyArray_GETPTR2(pyZ, k, 6));
  double y_wfc = *((double *)PyArray_GETPTR2(pyZ, k, 7));
  double y_T_amb = *((double *)PyArray_GETPTR2(pyZ, k, 8));
  double y_p_amb = *((double *)PyArray_GETPTR2(pyZ, k, 9));

  // Residual generator body
  W_fc = y_wfc; // e92
  p_amb = y_p_amb; // e94
  T_amb = y_T_amb; // e93
  u_wg = y_u_wg; // e91
  dwgdt_pos = (u_wg - wg_pos)/tau_wg; // e79
  omega_e = y_omega_e; // e89
  alpha_th = y_alpha_th; // e90
  Aeff_wg = Amax*Cd*wg_pos; // e78
  Aeff_th = A_0 + (43.0/9000.0)*M_PI*A_1*alpha_th + (1.0/45.0)*M_PI*A_1 + (1849.0/81000000.0)*pow(M_PI, 2)*A_2*pow(alpha_th, 2) + (43.0/202500.0)*pow(M_PI, 2)*A_2*alpha_th + (1.0/2025.0)*pow(M_PI, 2)*A_2; // e42
  T_in = CEva_cool - CEva_cool/lambda_af + T_im; // e44
  U_c = (1.0/2.0)*D_c*omega_tc; // e66
  p_em = R_exh*T_em*m_em/V_em; // e31
  p_im = R_air*T_im*m_im/V_im; // e26
  C_eta_vol = 9.9999999999999998e-13*a1*pow(max_fun(p_im, 25000), 4) + 1.0000000000000001e-9*a2*pow(max_fun(p_im, 25000), 3) + 9.9999999999999995e-7*a3*pow(max_fun(p_im, 25000), 2) + 0.001*a4*max_fun(p_im, 25000) + a5; // e46
  eta_vol = C_eta_vol*T_im*(r_c - pow(p_em/p_im, 1.0/gamma_exh))/(T_in*(r_c - 1)); // e45
  W_ac = (1.0/2.0)*V_D*eta_vol*omega_e*p_im/(M_PI*R_air*T_im*n_r); // e43
  W_e = W_ac + W_fc; // e57
  T_e = K_t*W_e + T0; // e58
  T_ti = (T_amb*exp(4*A_em*h_tot/(W_e*cp_exh)) - T_amb + T_e)*exp(-4*A_em*h_tot/(W_e*cp_exh)); // e59
  T_imcr = T_ic; // e6
  p_c = R_air*T_c*m_c/V_c; // e16
  p_af = R_air*T_af*m_af/V_af; // e11
  PI_cnolim = p_c/p_af; // e65
  PI_c = PI_c_fun(p_c, p_af); // e64
  PSI_c = 2*T_af*cp_air*(pow(PI_c, (gamma_air - 1)/gamma_air) - 1)/pow(U_c, 2); // e63
  PHI_model = PHI_model_fun(K1, K2, PSI_c); // e62
  W_c = W_c_fun(PI_cnolim, p_af, U_c, D_c, T_af, R_air, PHI_model, fix_gain); // e61
  W_ccorr = W_c*p_std*sqrt(T_af/T_std)/p_af; // e69
  eta_c = eta_c_fun(eta_cmax, eta_cmin, W_ccorr, W_ccorrmax, PI_c, PI_cmax, Q_c11, Q_c12, Q_c22); // e68
  T_cout = T_af*(pow(PI_c, (gamma_air - 1)/gamma_air) + eta_c - 1)/eta_c; // e67
  Tq_c = W_c*cp_air*(-T_af + T_cout)/omega_tc; // e60
  p_ic = R_air*T_ic*m_ic/V_ic; // e21
  W_ic = W_ic_fun(p_c, p_ic, plin_intercooler, H_intercooler, T_c); // e1
  dmdt_c = W_c - W_ic; // e17
  dTdt_c = (R_air*(-T_c*W_ic + T_cout*W_c) + W_c*cv_air*(-T_c + T_cout))/(cv_air*m_c); // e18
  T_fwd_flow_ic = max_fun(T_amb, T_c - max_fun(TOL, -Cic_1*T_amb + Cic_1*T_c - 1.0/2.0*Cic_2*pow(T_amb, 2) + (1.0/2.0)*Cic_2*pow(T_c, 2) - Cic_3*T_amb*W_ic + Cic_3*T_c*W_ic)); // e41
  PSI_th = PSI_th_fun(p_im, p_ic, gamma_air, PIli_th); // e4
  W_th = Aeff_th*PSI_th*p_ic/sqrt(R_air*T_ic); // e5
  dTdt_im = (R_air*(-T_im*W_ac + T_imcr*W_th) + W_th*cv_air*(-T_im + T_imcr))/(cv_air*m_im); // e28
  dmdt_ic = W_ic - W_th; // e22
  dTdt_ic = (R_air*(T_fwd_flow_ic*W_ic - T_ic*W_th) + W_ic*cv_air*(T_fwd_flow_ic - T_ic))/(cv_air*m_ic); // e23
  dmdt_im = -W_ac + W_th; // e27
  p_t = R_exh*T_t*m_t/V_t; // e36
  W_es = W_es_fun(p_amb, p_t, plin_exh, H_exhaust, T_t); // e3
  PI_wg = PI_wg_fun(p_t, p_em, gamma_air); // e7
  PSIli_wg = PSIli_wg_fun(PI_wg, PIli_wg, gamma_exh); // e8
  Tflow_wg = Tflow_wg_fun(p_t, p_em, T_em, T_t); // e10
  W_wg = Aeff_wg*PSIli_wg*p_em/sqrt(R_exh*Tflow_wg); // e9
  PI_t = PI_t_fun(p_t, p_em); // e75
  W_t = W_t_fun(p_em, k1, PI_t, k2, T_em); // e70
  W_twg = W_t + W_wg; // e77
  dmdt_em = W_e - W_twg; // e32
  dTdt_em = (R_exh*(-T_em*W_twg + T_ti*W_e) + W_e*cv_exh*(-T_em + T_ti))/(cv_exh*m_em); // e33
  dmdt_t = -W_es + W_twg; // e37
  dh_is = T_em*cp_exh*(1 - pow(PI_t, (gamma_exh - 1)/gamma_exh)); // e73
  eta_t = max_fun(TOL, min_fun(1 - TOL, (1000*sqrt(T_em)*W_t*a_eta_t_fun(omega_tc) + p_em*b_eta_t_fun(omega_tc))/(dh_is*p_em))); // e72
  T_tout = T_em*(pow(PI_t, (gamma_eg - 1)/gamma_eg)*eta_t - eta_t + 1); // e74
  T_turb = (T_tout*W_t + Tflow_wg*W_wg)/(W_t + W_wg); // e76
  dTdt_t = (R_exh*(-T_t*W_es + T_turb*W_twg) + W_twg*cv_exh*(-T_t + T_turb))/(cv_exh*m_t); // e38
  Tq_t = Tq_t_fun(gamma_eg, cp_eg, eta_t, W_t, T_em, PI_t, omega_tc); // e71
  domegadt_tc = (-Tq_c + Tq_t - omega_tc*xi_fric_tc)/J_tc; // e83
  W_af = W_af_fun(p_amb, p_af, plin_af, H_af, T_amb); // e2
  dmdt_af = W_af - W_c; // e12
  dTdt_af = (R_air*(-T_af*W_c + T_amb*W_af) + W_af*cv_air*(-T_af + T_amb))/(cv_air*m_af); // e13
   
  r[0] = T_ic - y_T_ic; // e87

  // Update integrator variables
  wg_pos = ApproxInt(dwgdt_pos, state->wg_pos, Ts); // e80
  T_im = ApproxInt(dTdt_im, state->T_im, Ts); // e30
  m_af = ApproxInt(dmdt_af, state->m_af, Ts); // e14
  T_af = ApproxInt(dTdt_af, state->T_af, Ts); // e15
  m_c = ApproxInt(dmdt_c, state->m_c, Ts); // e19
  T_c = ApproxInt(dTdt_c, state->T_c, Ts); // e20
  m_ic = ApproxInt(dmdt_ic, state->m_ic, Ts); // e24
  T_ic = ApproxInt(dTdt_ic, state->T_ic, Ts); // e25
  m_im = ApproxInt(dmdt_im, state->m_im, Ts); // e29
  m_em = ApproxInt(dmdt_em, state->m_em, Ts); // e34
  T_em = ApproxInt(dTdt_em, state->T_em, Ts); // e35
  m_t = ApproxInt(dmdt_t, state->m_t, Ts); // e39
  T_t = ApproxInt(dTdt_t, state->T_t, Ts); // e40
  omega_tc = ApproxInt(domegadt_tc, state->omega_tc, Ts); // e84

  // Update state variables
  state->wg_pos = wg_pos;
  state->T_im = T_im;
  state->m_af = m_af;
  state->T_af = T_af;
  state->m_c = m_c;
  state->T_c = T_c;
  state->m_ic = m_ic;
  state->T_ic = T_ic;
  state->m_im = m_im;
  state->m_em = m_em;
  state->T_em = T_em;
  state->m_t = m_t;
  state->T_t = T_t;
  state->omega_tc = omega_tc;
}

double
ApproxInt(double dx, double x0, double Ts)
{
  return x0 + Ts*dx;
}

void
GetParameters( PyObject *pyParams, Parameters* params )
{
  PyObject *H_af = PyDict_GetItemString(pyParams, "H_af");
  params->H_af = PyFloat_AsDouble(H_af);

  PyObject *plin_af = PyDict_GetItemString(pyParams, "plin_af");
  params->plin_af = PyFloat_AsDouble(plin_af);

  PyObject *H_exhaust = PyDict_GetItemString(pyParams, "H_exhaust");
  params->H_exhaust = PyFloat_AsDouble(H_exhaust);

  PyObject *plin_exh = PyDict_GetItemString(pyParams, "plin_exh");
  params->plin_exh = PyFloat_AsDouble(plin_exh);

  PyObject *H_intercooler = PyDict_GetItemString(pyParams, "H_intercooler");
  params->H_intercooler = PyFloat_AsDouble(H_intercooler);

  PyObject *plin_intercooler = PyDict_GetItemString(pyParams, "plin_intercooler");
  params->plin_intercooler = PyFloat_AsDouble(plin_intercooler);

  PyObject *PIli_th = PyDict_GetItemString(pyParams, "PIli_th");
  params->PIli_th = PyFloat_AsDouble(PIli_th);

  PyObject *gamma_air = PyDict_GetItemString(pyParams, "gamma_air");
  params->gamma_air = PyFloat_AsDouble(gamma_air);

  PyObject *PIli_wg = PyDict_GetItemString(pyParams, "PIli_wg");
  params->PIli_wg = PyFloat_AsDouble(PIli_wg);

  PyObject *gamma_exh = PyDict_GetItemString(pyParams, "gamma_exh");
  params->gamma_exh = PyFloat_AsDouble(gamma_exh);

  PyObject *R_air = PyDict_GetItemString(pyParams, "R_air");
  params->R_air = PyFloat_AsDouble(R_air);

  PyObject *cp_air = PyDict_GetItemString(pyParams, "cp_air");
  params->cp_air = PyFloat_AsDouble(cp_air);

  PyObject *V_af = PyDict_GetItemString(pyParams, "V_af");
  params->V_af = PyFloat_AsDouble(V_af);

  PyObject *V_c = PyDict_GetItemString(pyParams, "V_c");
  params->V_c = PyFloat_AsDouble(V_c);

  PyObject *V_ic = PyDict_GetItemString(pyParams, "V_ic");
  params->V_ic = PyFloat_AsDouble(V_ic);

  PyObject *V_im = PyDict_GetItemString(pyParams, "V_im");
  params->V_im = PyFloat_AsDouble(V_im);

  PyObject *R_exh = PyDict_GetItemString(pyParams, "R_exh");
  params->R_exh = PyFloat_AsDouble(R_exh);

  PyObject *cp_exh = PyDict_GetItemString(pyParams, "cp_exh");
  params->cp_exh = PyFloat_AsDouble(cp_exh);

  PyObject *lambda_af = PyDict_GetItemString(pyParams, "lambda_af");
  params->lambda_af = PyFloat_AsDouble(lambda_af);

  PyObject *n_r = PyDict_GetItemString(pyParams, "n_r");
  params->n_r = PyFloat_AsDouble(n_r);

  PyObject *r_c = PyDict_GetItemString(pyParams, "r_c");
  params->r_c = PyFloat_AsDouble(r_c);

  PyObject *V_D = PyDict_GetItemString(pyParams, "V_D");
  params->V_D = PyFloat_AsDouble(V_D);

  PyObject *CEva_cool = PyDict_GetItemString(pyParams, "CEva_cool");
  params->CEva_cool = PyFloat_AsDouble(CEva_cool);

  PyObject *D_c = PyDict_GetItemString(pyParams, "D_c");
  params->D_c = PyFloat_AsDouble(D_c);

  PyObject *K1 = PyDict_GetItemString(pyParams, "K1");
  params->K1 = PyFloat_AsDouble(K1);

  PyObject *K2 = PyDict_GetItemString(pyParams, "K2");
  params->K2 = PyFloat_AsDouble(K2);

  PyObject *fix_gain = PyDict_GetItemString(pyParams, "fix_gain");
  params->fix_gain = PyFloat_AsDouble(fix_gain);

  PyObject *eta_cmax = PyDict_GetItemString(pyParams, "eta_cmax");
  params->eta_cmax = PyFloat_AsDouble(eta_cmax);

  PyObject *eta_cmin = PyDict_GetItemString(pyParams, "eta_cmin");
  params->eta_cmin = PyFloat_AsDouble(eta_cmin);

  PyObject *T_std = PyDict_GetItemString(pyParams, "T_std");
  params->T_std = PyFloat_AsDouble(T_std);

  PyObject *k1 = PyDict_GetItemString(pyParams, "k1");
  params->k1 = PyFloat_AsDouble(k1);

  PyObject *k2 = PyDict_GetItemString(pyParams, "k2");
  params->k2 = PyFloat_AsDouble(k2);

  PyObject *cp_eg = PyDict_GetItemString(pyParams, "cp_eg");
  params->cp_eg = PyFloat_AsDouble(cp_eg);

  PyObject *gamma_eg = PyDict_GetItemString(pyParams, "gamma_eg");
  params->gamma_eg = PyFloat_AsDouble(gamma_eg);

  PyObject *tau_wg = PyDict_GetItemString(pyParams, "tau_wg");
  params->tau_wg = PyFloat_AsDouble(tau_wg);

  PyObject *h_tot = PyDict_GetItemString(pyParams, "h_tot");
  params->h_tot = PyFloat_AsDouble(h_tot);

  PyObject *Amax = PyDict_GetItemString(pyParams, "Amax");
  params->Amax = PyFloat_AsDouble(Amax);

  PyObject *A_0 = PyDict_GetItemString(pyParams, "A_0");
  params->A_0 = PyFloat_AsDouble(A_0);

  PyObject *A_1 = PyDict_GetItemString(pyParams, "A_1");
  params->A_1 = PyFloat_AsDouble(A_1);

  PyObject *A_2 = PyDict_GetItemString(pyParams, "A_2");
  params->A_2 = PyFloat_AsDouble(A_2);

  PyObject *J_tc = PyDict_GetItemString(pyParams, "J_tc");
  params->J_tc = PyFloat_AsDouble(J_tc);

  PyObject *xi_fric_tc = PyDict_GetItemString(pyParams, "xi_fric_tc");
  params->xi_fric_tc = PyFloat_AsDouble(xi_fric_tc);

  PyObject *V_em = PyDict_GetItemString(pyParams, "V_em");
  params->V_em = PyFloat_AsDouble(V_em);

  PyObject *V_t = PyDict_GetItemString(pyParams, "V_t");
  params->V_t = PyFloat_AsDouble(V_t);

  PyObject *p_std = PyDict_GetItemString(pyParams, "p_std");
  params->p_std = PyFloat_AsDouble(p_std);

  PyObject *a1 = PyDict_GetItemString(pyParams, "a1");
  params->a1 = PyFloat_AsDouble(a1);

  PyObject *a2 = PyDict_GetItemString(pyParams, "a2");
  params->a2 = PyFloat_AsDouble(a2);

  PyObject *a3 = PyDict_GetItemString(pyParams, "a3");
  params->a3 = PyFloat_AsDouble(a3);

  PyObject *a4 = PyDict_GetItemString(pyParams, "a4");
  params->a4 = PyFloat_AsDouble(a4);

  PyObject *a5 = PyDict_GetItemString(pyParams, "a5");
  params->a5 = PyFloat_AsDouble(a5);

  PyObject *Q_c11 = PyDict_GetItemString(pyParams, "Q_c11");
  params->Q_c11 = PyFloat_AsDouble(Q_c11);

  PyObject *Q_c12 = PyDict_GetItemString(pyParams, "Q_c12");
  params->Q_c12 = PyFloat_AsDouble(Q_c12);

  PyObject *Q_c22 = PyDict_GetItemString(pyParams, "Q_c22");
  params->Q_c22 = PyFloat_AsDouble(Q_c22);

  PyObject *Cd = PyDict_GetItemString(pyParams, "Cd");
  params->Cd = PyFloat_AsDouble(Cd);

  PyObject *PI_cmax = PyDict_GetItemString(pyParams, "PI_cmax");
  params->PI_cmax = PyFloat_AsDouble(PI_cmax);

  PyObject *cv_exh = PyDict_GetItemString(pyParams, "cv_exh");
  params->cv_exh = PyFloat_AsDouble(cv_exh);

  PyObject *cv_air = PyDict_GetItemString(pyParams, "cv_air");
  params->cv_air = PyFloat_AsDouble(cv_air);

  PyObject *W_ccorrmax = PyDict_GetItemString(pyParams, "W_ccorrmax");
  params->W_ccorrmax = PyFloat_AsDouble(W_ccorrmax);

  PyObject *A_em = PyDict_GetItemString(pyParams, "A_em");
  params->A_em = PyFloat_AsDouble(A_em);

  PyObject *K_t = PyDict_GetItemString(pyParams, "K_t");
  params->K_t = PyFloat_AsDouble(K_t);

  PyObject *T0 = PyDict_GetItemString(pyParams, "T0");
  params->T0 = PyFloat_AsDouble(T0);

  PyObject *Cic_1 = PyDict_GetItemString(pyParams, "Cic_1");
  params->Cic_1 = PyFloat_AsDouble(Cic_1);

  PyObject *Cic_2 = PyDict_GetItemString(pyParams, "Cic_2");
  params->Cic_2 = PyFloat_AsDouble(Cic_2);

  PyObject *Cic_3 = PyDict_GetItemString(pyParams, "Cic_3");
  params->Cic_3 = PyFloat_AsDouble(Cic_3);

  PyObject *TOL = PyDict_GetItemString(pyParams, "TOL");
  params->TOL = PyFloat_AsDouble(TOL);

}

void
GetState( PyObject *pyState, ResState* state )
{
  PyObject *wg_pos = PyDict_GetItemString(pyState, "wg_pos");
  state->wg_pos = PyFloat_AsDouble(wg_pos);

  PyObject *T_im = PyDict_GetItemString(pyState, "T_im");
  state->T_im = PyFloat_AsDouble(T_im);

  PyObject *m_af = PyDict_GetItemString(pyState, "m_af");
  state->m_af = PyFloat_AsDouble(m_af);

  PyObject *T_af = PyDict_GetItemString(pyState, "T_af");
  state->T_af = PyFloat_AsDouble(T_af);

  PyObject *m_c = PyDict_GetItemString(pyState, "m_c");
  state->m_c = PyFloat_AsDouble(m_c);

  PyObject *T_c = PyDict_GetItemString(pyState, "T_c");
  state->T_c = PyFloat_AsDouble(T_c);

  PyObject *m_ic = PyDict_GetItemString(pyState, "m_ic");
  state->m_ic = PyFloat_AsDouble(m_ic);

  PyObject *T_ic = PyDict_GetItemString(pyState, "T_ic");
  state->T_ic = PyFloat_AsDouble(T_ic);

  PyObject *m_im = PyDict_GetItemString(pyState, "m_im");
  state->m_im = PyFloat_AsDouble(m_im);

  PyObject *m_em = PyDict_GetItemString(pyState, "m_em");
  state->m_em = PyFloat_AsDouble(m_em);

  PyObject *T_em = PyDict_GetItemString(pyState, "T_em");
  state->T_em = PyFloat_AsDouble(T_em);

  PyObject *m_t = PyDict_GetItemString(pyState, "m_t");
  state->m_t = PyFloat_AsDouble(m_t);

  PyObject *T_t = PyDict_GetItemString(pyState, "T_t");
  state->T_t = PyFloat_AsDouble(T_t);

  PyObject *omega_tc = PyDict_GetItemString(pyState, "omega_tc");
  state->omega_tc = PyFloat_AsDouble(omega_tc);

}

struct module_state {
    PyObject *error;
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct module_state _state;
#endif

static PyObject *
error_out(PyObject *m) {
    struct module_state *st = GETSTATE(m);
    PyErr_SetString(st->error, "something bad happened");
    return NULL;
}

static PyMethodDef ResGen_4477_86_methods[] = {
    {"ResGen_4477_86",  ResGen_4477_86, METH_VARARGS, "Residual generator ResGen_4477_86"},
    {NULL, NULL}
};

#if PY_MAJOR_VERSION >= 3

static int ResGen_4477_86_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}

static int ResGen_4477_86_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}

static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "ResGen_4477_86",
        NULL,
        sizeof(struct module_state),
        ResGen_4477_86_methods,
        NULL,
        ResGen_4477_86_traverse,
        ResGen_4477_86_clear,
        NULL
};

#define INITERROR return NULL

PyMODINIT_FUNC
PyInit_ResGen_4477_86(void)

#else
#define INITERROR return

PyMODINIT_FUNC
initResGen_4477_86(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&moduledef);
#else
    PyObject *module = Py_InitModule("ResGen_4477_86", ResGen_4477_86_methods);
#endif

    if (module == NULL)
        INITERROR;
    struct module_state *st = GETSTATE(module);

    char errName[] = "ResGen_4477_86.Error";
    st->error = PyErr_NewException(errName, NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        INITERROR;
    }

    import_array();

#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
