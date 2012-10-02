/* Include files */

#include "blascompat32.h"
#include "ASV_pathplot_sfun.h"
#include "c1_ASV_pathplot.h"
#include "mwmathutil.h"
#define CHARTINSTANCE_CHARTNUMBER      (chartInstance->chartNumber)
#define CHARTINSTANCE_INSTANCENUMBER   (chartInstance->instanceNumber)
#include "ASV_pathplot_sfun_debug_macros.h"

/* Type Definitions */

/* Named Constants */

/* Variable Declarations */

/* Variable Definitions */
static const char * c1_debug_family_names[18] = { "nargin", "nargout", "Rho",
  "S1", "S2", "Theta", "Length", "Width", "RPM1", "RPM2", "dot_S1", "dot_S2",
  "Push_1", "Drag_1", "Drift_1", "Push_2", "Drag_2", "Drift_2" };

/* Function Declarations */
static void initialize_c1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct
  *chartInstance);
static void initialize_params_c1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct
  *chartInstance);
static void enable_c1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct
  *chartInstance);
static void disable_c1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct
  *chartInstance);
static void c1_update_debugger_state_c1_ASV_pathplot
  (SFc1_ASV_pathplotInstanceStruct *chartInstance);
static const mxArray *get_sim_state_c1_ASV_pathplot
  (SFc1_ASV_pathplotInstanceStruct *chartInstance);
static void set_sim_state_c1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct
  *chartInstance, const mxArray *c1_st);
static void finalize_c1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct
  *chartInstance);
static void sf_c1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct *chartInstance);
static void c1_chartstep_c1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct
  *chartInstance);
static void initSimStructsc1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct
  *chartInstance);
static void init_script_number_translation(uint32_T c1_machineNumber, uint32_T
  c1_chartNumber);
static const mxArray *c1_sf_marshallOut(void *chartInstanceVoid, void *c1_inData);
static real_T c1_emlrt_marshallIn(SFc1_ASV_pathplotInstanceStruct *chartInstance,
  const mxArray *c1_Drift_2, const char_T *c1_identifier);
static real_T c1_b_emlrt_marshallIn(SFc1_ASV_pathplotInstanceStruct
  *chartInstance, const mxArray *c1_u, const emlrtMsgIdentifier *c1_parentId);
static void c1_sf_marshallIn(void *chartInstanceVoid, const mxArray
  *c1_mxArrayInData, const char_T *c1_varName, void *c1_outData);
static const mxArray *c1_b_sf_marshallOut(void *chartInstanceVoid, void
  *c1_inData);
static int32_T c1_c_emlrt_marshallIn(SFc1_ASV_pathplotInstanceStruct
  *chartInstance, const mxArray *c1_u, const emlrtMsgIdentifier *c1_parentId);
static void c1_b_sf_marshallIn(void *chartInstanceVoid, const mxArray
  *c1_mxArrayInData, const char_T *c1_varName, void *c1_outData);
static uint8_T c1_d_emlrt_marshallIn(SFc1_ASV_pathplotInstanceStruct
  *chartInstance, const mxArray *c1_b_is_active_c1_ASV_pathplot, const char_T
  *c1_identifier);
static uint8_T c1_e_emlrt_marshallIn(SFc1_ASV_pathplotInstanceStruct
  *chartInstance, const mxArray *c1_u, const emlrtMsgIdentifier *c1_parentId);
static void init_dsm_address_info(SFc1_ASV_pathplotInstanceStruct *chartInstance);

/* Function Definitions */
static void initialize_c1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct
  *chartInstance)
{
  chartInstance->c1_sfEvent = CALL_EVENT;
  _sfTime_ = (real_T)ssGetT(chartInstance->S);
  chartInstance->c1_is_active_c1_ASV_pathplot = 0U;
}

static void initialize_params_c1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct
  *chartInstance)
{
}

static void enable_c1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct
  *chartInstance)
{
  _sfTime_ = (real_T)ssGetT(chartInstance->S);
}

static void disable_c1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct
  *chartInstance)
{
  _sfTime_ = (real_T)ssGetT(chartInstance->S);
}

static void c1_update_debugger_state_c1_ASV_pathplot
  (SFc1_ASV_pathplotInstanceStruct *chartInstance)
{
}

static const mxArray *get_sim_state_c1_ASV_pathplot
  (SFc1_ASV_pathplotInstanceStruct *chartInstance)
{
  const mxArray *c1_st;
  const mxArray *c1_y = NULL;
  real_T c1_hoistedGlobal;
  real_T c1_u;
  const mxArray *c1_b_y = NULL;
  real_T c1_b_hoistedGlobal;
  real_T c1_b_u;
  const mxArray *c1_c_y = NULL;
  real_T c1_c_hoistedGlobal;
  real_T c1_c_u;
  const mxArray *c1_d_y = NULL;
  real_T c1_d_hoistedGlobal;
  real_T c1_d_u;
  const mxArray *c1_e_y = NULL;
  real_T c1_e_hoistedGlobal;
  real_T c1_e_u;
  const mxArray *c1_f_y = NULL;
  real_T c1_f_hoistedGlobal;
  real_T c1_f_u;
  const mxArray *c1_g_y = NULL;
  real_T c1_g_hoistedGlobal;
  real_T c1_g_u;
  const mxArray *c1_h_y = NULL;
  real_T c1_h_hoistedGlobal;
  real_T c1_h_u;
  const mxArray *c1_i_y = NULL;
  uint8_T c1_i_hoistedGlobal;
  uint8_T c1_i_u;
  const mxArray *c1_j_y = NULL;
  real_T *c1_Drag_1;
  real_T *c1_Drag_2;
  real_T *c1_Drift_1;
  real_T *c1_Drift_2;
  real_T *c1_Push_1;
  real_T *c1_Push_2;
  real_T *c1_dot_S1;
  real_T *c1_dot_S2;
  c1_Drift_2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 8);
  c1_Drag_2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 7);
  c1_Push_2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 6);
  c1_Drift_1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 5);
  c1_Drag_1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 4);
  c1_Push_1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 3);
  c1_dot_S2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 2);
  c1_dot_S1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 1);
  c1_st = NULL;
  c1_st = NULL;
  c1_y = NULL;
  sf_mex_assign(&c1_y, sf_mex_createcellarray(9));
  c1_hoistedGlobal = *c1_Drag_1;
  c1_u = c1_hoistedGlobal;
  c1_b_y = NULL;
  sf_mex_assign(&c1_b_y, sf_mex_create("y", &c1_u, 0, 0U, 0U, 0U, 0));
  sf_mex_setcell(c1_y, 0, c1_b_y);
  c1_b_hoistedGlobal = *c1_Drag_2;
  c1_b_u = c1_b_hoistedGlobal;
  c1_c_y = NULL;
  sf_mex_assign(&c1_c_y, sf_mex_create("y", &c1_b_u, 0, 0U, 0U, 0U, 0));
  sf_mex_setcell(c1_y, 1, c1_c_y);
  c1_c_hoistedGlobal = *c1_Drift_1;
  c1_c_u = c1_c_hoistedGlobal;
  c1_d_y = NULL;
  sf_mex_assign(&c1_d_y, sf_mex_create("y", &c1_c_u, 0, 0U, 0U, 0U, 0));
  sf_mex_setcell(c1_y, 2, c1_d_y);
  c1_d_hoistedGlobal = *c1_Drift_2;
  c1_d_u = c1_d_hoistedGlobal;
  c1_e_y = NULL;
  sf_mex_assign(&c1_e_y, sf_mex_create("y", &c1_d_u, 0, 0U, 0U, 0U, 0));
  sf_mex_setcell(c1_y, 3, c1_e_y);
  c1_e_hoistedGlobal = *c1_Push_1;
  c1_e_u = c1_e_hoistedGlobal;
  c1_f_y = NULL;
  sf_mex_assign(&c1_f_y, sf_mex_create("y", &c1_e_u, 0, 0U, 0U, 0U, 0));
  sf_mex_setcell(c1_y, 4, c1_f_y);
  c1_f_hoistedGlobal = *c1_Push_2;
  c1_f_u = c1_f_hoistedGlobal;
  c1_g_y = NULL;
  sf_mex_assign(&c1_g_y, sf_mex_create("y", &c1_f_u, 0, 0U, 0U, 0U, 0));
  sf_mex_setcell(c1_y, 5, c1_g_y);
  c1_g_hoistedGlobal = *c1_dot_S1;
  c1_g_u = c1_g_hoistedGlobal;
  c1_h_y = NULL;
  sf_mex_assign(&c1_h_y, sf_mex_create("y", &c1_g_u, 0, 0U, 0U, 0U, 0));
  sf_mex_setcell(c1_y, 6, c1_h_y);
  c1_h_hoistedGlobal = *c1_dot_S2;
  c1_h_u = c1_h_hoistedGlobal;
  c1_i_y = NULL;
  sf_mex_assign(&c1_i_y, sf_mex_create("y", &c1_h_u, 0, 0U, 0U, 0U, 0));
  sf_mex_setcell(c1_y, 7, c1_i_y);
  c1_i_hoistedGlobal = chartInstance->c1_is_active_c1_ASV_pathplot;
  c1_i_u = c1_i_hoistedGlobal;
  c1_j_y = NULL;
  sf_mex_assign(&c1_j_y, sf_mex_create("y", &c1_i_u, 3, 0U, 0U, 0U, 0));
  sf_mex_setcell(c1_y, 8, c1_j_y);
  sf_mex_assign(&c1_st, c1_y);
  return c1_st;
}

static void set_sim_state_c1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct
  *chartInstance, const mxArray *c1_st)
{
  const mxArray *c1_u;
  real_T *c1_Drag_1;
  real_T *c1_Drag_2;
  real_T *c1_Drift_1;
  real_T *c1_Drift_2;
  real_T *c1_Push_1;
  real_T *c1_Push_2;
  real_T *c1_dot_S1;
  real_T *c1_dot_S2;
  c1_Drift_2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 8);
  c1_Drag_2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 7);
  c1_Push_2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 6);
  c1_Drift_1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 5);
  c1_Drag_1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 4);
  c1_Push_1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 3);
  c1_dot_S2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 2);
  c1_dot_S1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 1);
  chartInstance->c1_doneDoubleBufferReInit = TRUE;
  c1_u = sf_mex_dup(c1_st);
  *c1_Drag_1 = c1_emlrt_marshallIn(chartInstance, sf_mex_dup(sf_mex_getcell(c1_u,
    0)), "Drag_1");
  *c1_Drag_2 = c1_emlrt_marshallIn(chartInstance, sf_mex_dup(sf_mex_getcell(c1_u,
    1)), "Drag_2");
  *c1_Drift_1 = c1_emlrt_marshallIn(chartInstance, sf_mex_dup(sf_mex_getcell
    (c1_u, 2)), "Drift_1");
  *c1_Drift_2 = c1_emlrt_marshallIn(chartInstance, sf_mex_dup(sf_mex_getcell
    (c1_u, 3)), "Drift_2");
  *c1_Push_1 = c1_emlrt_marshallIn(chartInstance, sf_mex_dup(sf_mex_getcell(c1_u,
    4)), "Push_1");
  *c1_Push_2 = c1_emlrt_marshallIn(chartInstance, sf_mex_dup(sf_mex_getcell(c1_u,
    5)), "Push_2");
  *c1_dot_S1 = c1_emlrt_marshallIn(chartInstance, sf_mex_dup(sf_mex_getcell(c1_u,
    6)), "dot_S1");
  *c1_dot_S2 = c1_emlrt_marshallIn(chartInstance, sf_mex_dup(sf_mex_getcell(c1_u,
    7)), "dot_S2");
  chartInstance->c1_is_active_c1_ASV_pathplot = c1_d_emlrt_marshallIn
    (chartInstance, sf_mex_dup(sf_mex_getcell(c1_u, 8)),
     "is_active_c1_ASV_pathplot");
  sf_mex_destroy(&c1_u);
  c1_update_debugger_state_c1_ASV_pathplot(chartInstance);
  sf_mex_destroy(&c1_st);
}

static void finalize_c1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct
  *chartInstance)
{
}

static void sf_c1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct *chartInstance)
{
  real_T *c1_Rho;
  real_T *c1_dot_S1;
  real_T *c1_S1;
  real_T *c1_S2;
  real_T *c1_Theta;
  real_T *c1_Length;
  real_T *c1_Width;
  real_T *c1_dot_S2;
  real_T *c1_Push_1;
  real_T *c1_RPM1;
  real_T *c1_RPM2;
  real_T *c1_Drag_1;
  real_T *c1_Drift_1;
  real_T *c1_Push_2;
  real_T *c1_Drag_2;
  real_T *c1_Drift_2;
  c1_Drift_2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 8);
  c1_Drag_2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 7);
  c1_Push_2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 6);
  c1_Drift_1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 5);
  c1_Drag_1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 4);
  c1_RPM2 = (real_T *)ssGetInputPortSignal(chartInstance->S, 7);
  c1_RPM1 = (real_T *)ssGetInputPortSignal(chartInstance->S, 6);
  c1_Push_1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 3);
  c1_dot_S2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 2);
  c1_Width = (real_T *)ssGetInputPortSignal(chartInstance->S, 5);
  c1_Length = (real_T *)ssGetInputPortSignal(chartInstance->S, 4);
  c1_Theta = (real_T *)ssGetInputPortSignal(chartInstance->S, 3);
  c1_S2 = (real_T *)ssGetInputPortSignal(chartInstance->S, 2);
  c1_S1 = (real_T *)ssGetInputPortSignal(chartInstance->S, 1);
  c1_dot_S1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 1);
  c1_Rho = (real_T *)ssGetInputPortSignal(chartInstance->S, 0);
  _sfTime_ = (real_T)ssGetT(chartInstance->S);
  _SFD_CC_CALL(CHART_ENTER_SFUNCTION_TAG, 0U, chartInstance->c1_sfEvent);
  _SFD_DATA_RANGE_CHECK(*c1_Rho, 0U);
  _SFD_DATA_RANGE_CHECK(*c1_dot_S1, 1U);
  _SFD_DATA_RANGE_CHECK(*c1_S1, 2U);
  _SFD_DATA_RANGE_CHECK(*c1_S2, 3U);
  _SFD_DATA_RANGE_CHECK(*c1_Theta, 4U);
  _SFD_DATA_RANGE_CHECK(*c1_Length, 5U);
  _SFD_DATA_RANGE_CHECK(*c1_Width, 6U);
  _SFD_DATA_RANGE_CHECK(*c1_dot_S2, 7U);
  _SFD_DATA_RANGE_CHECK(*c1_Push_1, 8U);
  _SFD_DATA_RANGE_CHECK(*c1_RPM1, 9U);
  _SFD_DATA_RANGE_CHECK(*c1_RPM2, 10U);
  _SFD_DATA_RANGE_CHECK(*c1_Drag_1, 11U);
  _SFD_DATA_RANGE_CHECK(*c1_Drift_1, 12U);
  _SFD_DATA_RANGE_CHECK(*c1_Push_2, 13U);
  _SFD_DATA_RANGE_CHECK(*c1_Drag_2, 14U);
  _SFD_DATA_RANGE_CHECK(*c1_Drift_2, 15U);
  chartInstance->c1_sfEvent = CALL_EVENT;
  c1_chartstep_c1_ASV_pathplot(chartInstance);
  sf_debug_check_for_state_inconsistency(_ASV_pathplotMachineNumber_,
    chartInstance->chartNumber, chartInstance->instanceNumber);
}

static void c1_chartstep_c1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct
  *chartInstance)
{
  real_T c1_hoistedGlobal;
  real_T c1_b_hoistedGlobal;
  real_T c1_c_hoistedGlobal;
  real_T c1_d_hoistedGlobal;
  real_T c1_e_hoistedGlobal;
  real_T c1_f_hoistedGlobal;
  real_T c1_g_hoistedGlobal;
  real_T c1_h_hoistedGlobal;
  real_T c1_Rho;
  real_T c1_S1;
  real_T c1_S2;
  real_T c1_Theta;
  real_T c1_Length;
  real_T c1_Width;
  real_T c1_RPM1;
  real_T c1_RPM2;
  uint32_T c1_debug_family_var_map[18];
  real_T c1_nargin = 8.0;
  real_T c1_nargout = 8.0;
  real_T c1_dot_S1;
  real_T c1_dot_S2;
  real_T c1_Push_1;
  real_T c1_Drag_1;
  real_T c1_Drift_1;
  real_T c1_Push_2;
  real_T c1_Drag_2;
  real_T c1_Drift_2;
  real_T c1_x;
  real_T c1_b_x;
  real_T c1_a;
  real_T c1_b;
  real_T c1_c_x;
  real_T c1_d_x;
  real_T c1_e_x;
  real_T c1_f_x;
  real_T c1_y;
  real_T c1_b_a;
  real_T c1_b_b;
  real_T c1_b_y;
  real_T c1_c_b;
  real_T c1_c_y;
  real_T c1_g_x;
  real_T c1_h_x;
  real_T c1_c_a;
  real_T c1_d_b;
  real_T c1_d_y;
  real_T c1_d_a;
  real_T c1_e_b;
  real_T c1_e_y;
  real_T c1_e_a;
  real_T c1_f_b;
  real_T c1_f_a;
  real_T c1_g_b;
  real_T c1_f_y;
  real_T c1_g_a;
  real_T c1_h_b;
  real_T c1_g_y;
  real_T c1_i_x;
  real_T c1_j_x;
  real_T c1_k_x;
  real_T c1_l_x;
  real_T c1_h_y;
  real_T c1_h_a;
  real_T c1_i_b;
  real_T c1_m_x;
  real_T c1_n_x;
  real_T c1_i_a;
  real_T c1_j_b;
  real_T c1_o_x;
  real_T c1_p_x;
  real_T c1_q_x;
  real_T c1_r_x;
  real_T c1_i_y;
  real_T c1_j_a;
  real_T c1_k_b;
  real_T c1_j_y;
  real_T c1_l_b;
  real_T c1_k_y;
  real_T c1_s_x;
  real_T c1_t_x;
  real_T c1_k_a;
  real_T c1_m_b;
  real_T c1_l_y;
  real_T c1_l_a;
  real_T c1_n_b;
  real_T c1_m_y;
  real_T c1_m_a;
  real_T c1_o_b;
  real_T c1_n_a;
  real_T c1_p_b;
  real_T c1_n_y;
  real_T c1_o_a;
  real_T c1_q_b;
  real_T c1_o_y;
  real_T c1_u_x;
  real_T c1_v_x;
  real_T c1_w_x;
  real_T c1_x_x;
  real_T c1_p_y;
  real_T c1_p_a;
  real_T c1_r_b;
  real_T *c1_b_Rho;
  real_T *c1_b_S1;
  real_T *c1_b_S2;
  real_T *c1_b_Theta;
  real_T *c1_b_Length;
  real_T *c1_b_Width;
  real_T *c1_b_RPM1;
  real_T *c1_b_RPM2;
  real_T *c1_b_dot_S1;
  real_T *c1_b_dot_S2;
  real_T *c1_b_Push_1;
  real_T *c1_b_Drag_1;
  real_T *c1_b_Drift_1;
  real_T *c1_b_Push_2;
  real_T *c1_b_Drag_2;
  real_T *c1_b_Drift_2;
  c1_b_Drift_2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 8);
  c1_b_Drag_2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 7);
  c1_b_Push_2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 6);
  c1_b_Drift_1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 5);
  c1_b_Drag_1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 4);
  c1_b_RPM2 = (real_T *)ssGetInputPortSignal(chartInstance->S, 7);
  c1_b_RPM1 = (real_T *)ssGetInputPortSignal(chartInstance->S, 6);
  c1_b_Push_1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 3);
  c1_b_dot_S2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 2);
  c1_b_Width = (real_T *)ssGetInputPortSignal(chartInstance->S, 5);
  c1_b_Length = (real_T *)ssGetInputPortSignal(chartInstance->S, 4);
  c1_b_Theta = (real_T *)ssGetInputPortSignal(chartInstance->S, 3);
  c1_b_S2 = (real_T *)ssGetInputPortSignal(chartInstance->S, 2);
  c1_b_S1 = (real_T *)ssGetInputPortSignal(chartInstance->S, 1);
  c1_b_dot_S1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 1);
  c1_b_Rho = (real_T *)ssGetInputPortSignal(chartInstance->S, 0);
  _SFD_CC_CALL(CHART_ENTER_DURING_FUNCTION_TAG, 0U, chartInstance->c1_sfEvent);
  c1_hoistedGlobal = *c1_b_Rho;
  c1_b_hoistedGlobal = *c1_b_S1;
  c1_c_hoistedGlobal = *c1_b_S2;
  c1_d_hoistedGlobal = *c1_b_Theta;
  c1_e_hoistedGlobal = *c1_b_Length;
  c1_f_hoistedGlobal = *c1_b_Width;
  c1_g_hoistedGlobal = *c1_b_RPM1;
  c1_h_hoistedGlobal = *c1_b_RPM2;
  c1_Rho = c1_hoistedGlobal;
  c1_S1 = c1_b_hoistedGlobal;
  c1_S2 = c1_c_hoistedGlobal;
  c1_Theta = c1_d_hoistedGlobal;
  c1_Length = c1_e_hoistedGlobal;
  c1_Width = c1_f_hoistedGlobal;
  c1_RPM1 = c1_g_hoistedGlobal;
  c1_RPM2 = c1_h_hoistedGlobal;
  sf_debug_symbol_scope_push_eml(0U, 18U, 18U, c1_debug_family_names,
    c1_debug_family_var_map);
  sf_debug_symbol_scope_add_eml_importable(&c1_nargin, 0U, c1_sf_marshallOut,
    c1_sf_marshallIn);
  sf_debug_symbol_scope_add_eml_importable(&c1_nargout, 1U, c1_sf_marshallOut,
    c1_sf_marshallIn);
  sf_debug_symbol_scope_add_eml(&c1_Rho, 2U, c1_sf_marshallOut);
  sf_debug_symbol_scope_add_eml(&c1_S1, 3U, c1_sf_marshallOut);
  sf_debug_symbol_scope_add_eml(&c1_S2, 4U, c1_sf_marshallOut);
  sf_debug_symbol_scope_add_eml(&c1_Theta, 5U, c1_sf_marshallOut);
  sf_debug_symbol_scope_add_eml(&c1_Length, 6U, c1_sf_marshallOut);
  sf_debug_symbol_scope_add_eml(&c1_Width, 7U, c1_sf_marshallOut);
  sf_debug_symbol_scope_add_eml(&c1_RPM1, 8U, c1_sf_marshallOut);
  sf_debug_symbol_scope_add_eml(&c1_RPM2, 9U, c1_sf_marshallOut);
  sf_debug_symbol_scope_add_eml_importable(&c1_dot_S1, 10U, c1_sf_marshallOut,
    c1_sf_marshallIn);
  sf_debug_symbol_scope_add_eml_importable(&c1_dot_S2, 11U, c1_sf_marshallOut,
    c1_sf_marshallIn);
  sf_debug_symbol_scope_add_eml_importable(&c1_Push_1, 12U, c1_sf_marshallOut,
    c1_sf_marshallIn);
  sf_debug_symbol_scope_add_eml_importable(&c1_Drag_1, 13U, c1_sf_marshallOut,
    c1_sf_marshallIn);
  sf_debug_symbol_scope_add_eml_importable(&c1_Drift_1, 14U, c1_sf_marshallOut,
    c1_sf_marshallIn);
  sf_debug_symbol_scope_add_eml_importable(&c1_Push_2, 15U, c1_sf_marshallOut,
    c1_sf_marshallIn);
  sf_debug_symbol_scope_add_eml_importable(&c1_Drag_2, 16U, c1_sf_marshallOut,
    c1_sf_marshallIn);
  sf_debug_symbol_scope_add_eml_importable(&c1_Drift_2, 17U, c1_sf_marshallOut,
    c1_sf_marshallIn);
  CV_EML_FCN(0, 0);
  _SFD_EML_CALL(0U, chartInstance->c1_sfEvent, 4);
  c1_x = c1_Theta;
  c1_b_x = c1_x;
  c1_b_x = muDoubleScalarSin(c1_b_x);
  c1_a = c1_RPM1 + c1_RPM2;
  c1_b = c1_b_x;
  c1_Push_1 = c1_a * c1_b;
  _SFD_EML_CALL(0U, chartInstance->c1_sfEvent, 5);
  c1_c_x = c1_Theta;
  c1_d_x = c1_c_x;
  c1_d_x = muDoubleScalarCos(c1_d_x);
  c1_e_x = c1_d_x;
  c1_f_x = c1_e_x;
  c1_y = muDoubleScalarAbs(c1_f_x);
  c1_b_a = c1_S1;
  c1_b_b = c1_y;
  c1_b_y = c1_b_a * c1_b_b;
  c1_c_b = c1_S2;
  c1_c_y = 0.1 * c1_c_b;
  c1_g_x = c1_Theta;
  c1_h_x = c1_g_x;
  c1_h_x = muDoubleScalarSin(c1_h_x);
  c1_c_a = c1_c_y;
  c1_d_b = c1_h_x;
  c1_d_y = c1_c_a * c1_d_b;
  c1_d_a = c1_b_y - c1_d_y;
  c1_e_b = c1_Rho;
  c1_e_y = c1_d_a * c1_e_b;
  c1_e_a = c1_e_y;
  c1_f_b = c1_Length;
  c1_Drift_1 = c1_e_a * c1_f_b;
  _SFD_EML_CALL(0U, chartInstance->c1_sfEvent, 6);
  c1_f_a = c1_Rho;
  c1_g_b = c1_Width;
  c1_f_y = c1_f_a * c1_g_b;
  c1_g_a = c1_f_y;
  c1_h_b = c1_S1;
  c1_g_y = c1_g_a * c1_h_b;
  c1_i_x = c1_Theta;
  c1_j_x = c1_i_x;
  c1_j_x = muDoubleScalarSin(c1_j_x);
  c1_k_x = c1_j_x;
  c1_l_x = c1_k_x;
  c1_h_y = muDoubleScalarAbs(c1_l_x);
  c1_h_a = c1_g_y;
  c1_i_b = c1_h_y;
  c1_Drag_1 = c1_h_a * c1_i_b;
  _SFD_EML_CALL(0U, chartInstance->c1_sfEvent, 8);
  c1_dot_S1 = (c1_Push_1 - c1_Drag_1) - c1_Drift_1;
  _SFD_EML_CALL(0U, chartInstance->c1_sfEvent, 10);
  c1_m_x = c1_Theta;
  c1_n_x = c1_m_x;
  c1_n_x = muDoubleScalarCos(c1_n_x);
  c1_i_a = c1_RPM1 + c1_RPM2;
  c1_j_b = c1_n_x;
  c1_Push_2 = c1_i_a * c1_j_b;
  _SFD_EML_CALL(0U, chartInstance->c1_sfEvent, 11);
  c1_o_x = c1_Theta;
  c1_p_x = c1_o_x;
  c1_p_x = muDoubleScalarSin(c1_p_x);
  c1_q_x = c1_p_x;
  c1_r_x = c1_q_x;
  c1_i_y = muDoubleScalarAbs(c1_r_x);
  c1_j_a = c1_S2;
  c1_k_b = c1_i_y;
  c1_j_y = c1_j_a * c1_k_b;
  c1_l_b = c1_S1;
  c1_k_y = 0.1 * c1_l_b;
  c1_s_x = c1_Theta;
  c1_t_x = c1_s_x;
  c1_t_x = muDoubleScalarSin(c1_t_x);
  c1_k_a = c1_k_y;
  c1_m_b = c1_t_x;
  c1_l_y = c1_k_a * c1_m_b;
  c1_l_a = c1_j_y - c1_l_y;
  c1_n_b = c1_Rho;
  c1_m_y = c1_l_a * c1_n_b;
  c1_m_a = c1_m_y;
  c1_o_b = c1_Length;
  c1_Drift_2 = c1_m_a * c1_o_b;
  _SFD_EML_CALL(0U, chartInstance->c1_sfEvent, 12);
  c1_n_a = c1_Rho;
  c1_p_b = c1_Width;
  c1_n_y = c1_n_a * c1_p_b;
  c1_o_a = c1_n_y;
  c1_q_b = c1_S2;
  c1_o_y = c1_o_a * c1_q_b;
  c1_u_x = c1_Theta;
  c1_v_x = c1_u_x;
  c1_v_x = muDoubleScalarCos(c1_v_x);
  c1_w_x = c1_v_x;
  c1_x_x = c1_w_x;
  c1_p_y = muDoubleScalarAbs(c1_x_x);
  c1_p_a = c1_o_y;
  c1_r_b = c1_p_y;
  c1_Drag_2 = c1_p_a * c1_r_b;
  _SFD_EML_CALL(0U, chartInstance->c1_sfEvent, 14);
  c1_dot_S2 = (c1_Push_2 - c1_Drag_2) - c1_Drift_2;
  _SFD_EML_CALL(0U, chartInstance->c1_sfEvent, -14);
  sf_debug_symbol_scope_pop();
  *c1_b_dot_S1 = c1_dot_S1;
  *c1_b_dot_S2 = c1_dot_S2;
  *c1_b_Push_1 = c1_Push_1;
  *c1_b_Drag_1 = c1_Drag_1;
  *c1_b_Drift_1 = c1_Drift_1;
  *c1_b_Push_2 = c1_Push_2;
  *c1_b_Drag_2 = c1_Drag_2;
  *c1_b_Drift_2 = c1_Drift_2;
  _SFD_CC_CALL(EXIT_OUT_OF_FUNCTION_TAG, 0U, chartInstance->c1_sfEvent);
}

static void initSimStructsc1_ASV_pathplot(SFc1_ASV_pathplotInstanceStruct
  *chartInstance)
{
}

static void init_script_number_translation(uint32_T c1_machineNumber, uint32_T
  c1_chartNumber)
{
}

static const mxArray *c1_sf_marshallOut(void *chartInstanceVoid, void *c1_inData)
{
  const mxArray *c1_mxArrayOutData = NULL;
  real_T c1_u;
  const mxArray *c1_y = NULL;
  SFc1_ASV_pathplotInstanceStruct *chartInstance;
  chartInstance = (SFc1_ASV_pathplotInstanceStruct *)chartInstanceVoid;
  c1_mxArrayOutData = NULL;
  c1_u = *(real_T *)c1_inData;
  c1_y = NULL;
  sf_mex_assign(&c1_y, sf_mex_create("y", &c1_u, 0, 0U, 0U, 0U, 0));
  sf_mex_assign(&c1_mxArrayOutData, c1_y);
  return c1_mxArrayOutData;
}

static real_T c1_emlrt_marshallIn(SFc1_ASV_pathplotInstanceStruct *chartInstance,
  const mxArray *c1_Drift_2, const char_T *c1_identifier)
{
  real_T c1_y;
  emlrtMsgIdentifier c1_thisId;
  c1_thisId.fIdentifier = c1_identifier;
  c1_thisId.fParent = NULL;
  c1_y = c1_b_emlrt_marshallIn(chartInstance, sf_mex_dup(c1_Drift_2), &c1_thisId);
  sf_mex_destroy(&c1_Drift_2);
  return c1_y;
}

static real_T c1_b_emlrt_marshallIn(SFc1_ASV_pathplotInstanceStruct
  *chartInstance, const mxArray *c1_u, const emlrtMsgIdentifier *c1_parentId)
{
  real_T c1_y;
  real_T c1_d0;
  sf_mex_import(c1_parentId, sf_mex_dup(c1_u), &c1_d0, 1, 0, 0U, 0, 0U, 0);
  c1_y = c1_d0;
  sf_mex_destroy(&c1_u);
  return c1_y;
}

static void c1_sf_marshallIn(void *chartInstanceVoid, const mxArray
  *c1_mxArrayInData, const char_T *c1_varName, void *c1_outData)
{
  const mxArray *c1_Drift_2;
  const char_T *c1_identifier;
  emlrtMsgIdentifier c1_thisId;
  real_T c1_y;
  SFc1_ASV_pathplotInstanceStruct *chartInstance;
  chartInstance = (SFc1_ASV_pathplotInstanceStruct *)chartInstanceVoid;
  c1_Drift_2 = sf_mex_dup(c1_mxArrayInData);
  c1_identifier = c1_varName;
  c1_thisId.fIdentifier = c1_identifier;
  c1_thisId.fParent = NULL;
  c1_y = c1_b_emlrt_marshallIn(chartInstance, sf_mex_dup(c1_Drift_2), &c1_thisId);
  sf_mex_destroy(&c1_Drift_2);
  *(real_T *)c1_outData = c1_y;
  sf_mex_destroy(&c1_mxArrayInData);
}

const mxArray *sf_c1_ASV_pathplot_get_eml_resolved_functions_info(void)
{
  const mxArray *c1_nameCaptureInfo;
  c1_ResolvedFunctionInfo c1_info[7];
  c1_ResolvedFunctionInfo (*c1_b_info)[7];
  const mxArray *c1_m0 = NULL;
  int32_T c1_i0;
  c1_ResolvedFunctionInfo *c1_r0;
  c1_nameCaptureInfo = NULL;
  c1_nameCaptureInfo = NULL;
  c1_b_info = (c1_ResolvedFunctionInfo (*)[7])c1_info;
  (*c1_b_info)[0].context = "";
  (*c1_b_info)[0].name = "sin";
  (*c1_b_info)[0].dominantType = "double";
  (*c1_b_info)[0].resolved =
    "[ILXE]$matlabroot$/toolbox/eml/lib/matlab/elfun/sin.m";
  (*c1_b_info)[0].fileTimeLo = 907391744U;
  (*c1_b_info)[0].fileTimeHi = 30108011U;
  (*c1_b_info)[0].mFileTimeLo = 0U;
  (*c1_b_info)[0].mFileTimeHi = 0U;
  (*c1_b_info)[1].context =
    "[ILXE]$matlabroot$/toolbox/eml/lib/matlab/elfun/sin.m";
  (*c1_b_info)[1].name = "eml_scalar_sin";
  (*c1_b_info)[1].dominantType = "double";
  (*c1_b_info)[1].resolved =
    "[ILXE]$matlabroot$/toolbox/eml/lib/matlab/elfun/eml_scalar_sin.m";
  (*c1_b_info)[1].fileTimeLo = 767391744U;
  (*c1_b_info)[1].fileTimeHi = 30108011U;
  (*c1_b_info)[1].mFileTimeLo = 0U;
  (*c1_b_info)[1].mFileTimeHi = 0U;
  (*c1_b_info)[2].context = "";
  (*c1_b_info)[2].name = "mtimes";
  (*c1_b_info)[2].dominantType = "double";
  (*c1_b_info)[2].resolved =
    "[ILXE]$matlabroot$/toolbox/eml/lib/matlab/ops/mtimes.m";
  (*c1_b_info)[2].fileTimeLo = 3573034496U;
  (*c1_b_info)[2].fileTimeHi = 30114299U;
  (*c1_b_info)[2].mFileTimeLo = 0U;
  (*c1_b_info)[2].mFileTimeHi = 0U;
  (*c1_b_info)[3].context = "";
  (*c1_b_info)[3].name = "cos";
  (*c1_b_info)[3].dominantType = "double";
  (*c1_b_info)[3].resolved =
    "[ILXE]$matlabroot$/toolbox/eml/lib/matlab/elfun/cos.m";
  (*c1_b_info)[3].fileTimeLo = 467391744U;
  (*c1_b_info)[3].fileTimeHi = 30108011U;
  (*c1_b_info)[3].mFileTimeLo = 0U;
  (*c1_b_info)[3].mFileTimeHi = 0U;
  (*c1_b_info)[4].context =
    "[ILXE]$matlabroot$/toolbox/eml/lib/matlab/elfun/cos.m";
  (*c1_b_info)[4].name = "eml_scalar_cos";
  (*c1_b_info)[4].dominantType = "double";
  (*c1_b_info)[4].resolved =
    "[ILXE]$matlabroot$/toolbox/eml/lib/matlab/elfun/eml_scalar_cos.m";
  (*c1_b_info)[4].fileTimeLo = 627391744U;
  (*c1_b_info)[4].fileTimeHi = 30108011U;
  (*c1_b_info)[4].mFileTimeLo = 0U;
  (*c1_b_info)[4].mFileTimeHi = 0U;
  (*c1_b_info)[5].context = "";
  (*c1_b_info)[5].name = "abs";
  (*c1_b_info)[5].dominantType = "double";
  (*c1_b_info)[5].resolved =
    "[ILXE]$matlabroot$/toolbox/eml/lib/matlab/elfun/abs.m";
  (*c1_b_info)[5].fileTimeLo = 347391744U;
  (*c1_b_info)[5].fileTimeHi = 30108011U;
  (*c1_b_info)[5].mFileTimeLo = 0U;
  (*c1_b_info)[5].mFileTimeHi = 0U;
  (*c1_b_info)[6].context =
    "[ILXE]$matlabroot$/toolbox/eml/lib/matlab/elfun/abs.m";
  (*c1_b_info)[6].name = "eml_scalar_abs";
  (*c1_b_info)[6].dominantType = "double";
  (*c1_b_info)[6].resolved =
    "[ILXE]$matlabroot$/toolbox/eml/lib/matlab/elfun/eml_scalar_abs.m";
  (*c1_b_info)[6].fileTimeLo = 527391744U;
  (*c1_b_info)[6].fileTimeHi = 30108011U;
  (*c1_b_info)[6].mFileTimeLo = 0U;
  (*c1_b_info)[6].mFileTimeHi = 0U;
  sf_mex_assign(&c1_m0, sf_mex_createstruct("nameCaptureInfo", 1, 7));
  for (c1_i0 = 0; c1_i0 < 7; c1_i0++) {
    c1_r0 = &c1_info[c1_i0];
    sf_mex_addfield(c1_m0, sf_mex_create("nameCaptureInfo", c1_r0->context, 15,
      0U, 0U, 0U, 2, 1, strlen(c1_r0->context)), "context", "nameCaptureInfo",
                    c1_i0);
    sf_mex_addfield(c1_m0, sf_mex_create("nameCaptureInfo", c1_r0->name, 15, 0U,
      0U, 0U, 2, 1, strlen(c1_r0->name)), "name", "nameCaptureInfo", c1_i0);
    sf_mex_addfield(c1_m0, sf_mex_create("nameCaptureInfo", c1_r0->dominantType,
      15, 0U, 0U, 0U, 2, 1, strlen(c1_r0->dominantType)), "dominantType",
                    "nameCaptureInfo", c1_i0);
    sf_mex_addfield(c1_m0, sf_mex_create("nameCaptureInfo", c1_r0->resolved, 15,
      0U, 0U, 0U, 2, 1, strlen(c1_r0->resolved)), "resolved", "nameCaptureInfo",
                    c1_i0);
    sf_mex_addfield(c1_m0, sf_mex_create("nameCaptureInfo", &c1_r0->fileTimeLo,
      7, 0U, 0U, 0U, 0), "fileTimeLo", "nameCaptureInfo", c1_i0);
    sf_mex_addfield(c1_m0, sf_mex_create("nameCaptureInfo", &c1_r0->fileTimeHi,
      7, 0U, 0U, 0U, 0), "fileTimeHi", "nameCaptureInfo", c1_i0);
    sf_mex_addfield(c1_m0, sf_mex_create("nameCaptureInfo", &c1_r0->mFileTimeLo,
      7, 0U, 0U, 0U, 0), "mFileTimeLo", "nameCaptureInfo", c1_i0);
    sf_mex_addfield(c1_m0, sf_mex_create("nameCaptureInfo", &c1_r0->mFileTimeHi,
      7, 0U, 0U, 0U, 0), "mFileTimeHi", "nameCaptureInfo", c1_i0);
  }

  sf_mex_assign(&c1_nameCaptureInfo, c1_m0);
  return c1_nameCaptureInfo;
}

static const mxArray *c1_b_sf_marshallOut(void *chartInstanceVoid, void
  *c1_inData)
{
  const mxArray *c1_mxArrayOutData = NULL;
  int32_T c1_u;
  const mxArray *c1_y = NULL;
  SFc1_ASV_pathplotInstanceStruct *chartInstance;
  chartInstance = (SFc1_ASV_pathplotInstanceStruct *)chartInstanceVoid;
  c1_mxArrayOutData = NULL;
  c1_u = *(int32_T *)c1_inData;
  c1_y = NULL;
  sf_mex_assign(&c1_y, sf_mex_create("y", &c1_u, 6, 0U, 0U, 0U, 0));
  sf_mex_assign(&c1_mxArrayOutData, c1_y);
  return c1_mxArrayOutData;
}

static int32_T c1_c_emlrt_marshallIn(SFc1_ASV_pathplotInstanceStruct
  *chartInstance, const mxArray *c1_u, const emlrtMsgIdentifier *c1_parentId)
{
  int32_T c1_y;
  int32_T c1_i1;
  sf_mex_import(c1_parentId, sf_mex_dup(c1_u), &c1_i1, 1, 6, 0U, 0, 0U, 0);
  c1_y = c1_i1;
  sf_mex_destroy(&c1_u);
  return c1_y;
}

static void c1_b_sf_marshallIn(void *chartInstanceVoid, const mxArray
  *c1_mxArrayInData, const char_T *c1_varName, void *c1_outData)
{
  const mxArray *c1_b_sfEvent;
  const char_T *c1_identifier;
  emlrtMsgIdentifier c1_thisId;
  int32_T c1_y;
  SFc1_ASV_pathplotInstanceStruct *chartInstance;
  chartInstance = (SFc1_ASV_pathplotInstanceStruct *)chartInstanceVoid;
  c1_b_sfEvent = sf_mex_dup(c1_mxArrayInData);
  c1_identifier = c1_varName;
  c1_thisId.fIdentifier = c1_identifier;
  c1_thisId.fParent = NULL;
  c1_y = c1_c_emlrt_marshallIn(chartInstance, sf_mex_dup(c1_b_sfEvent),
    &c1_thisId);
  sf_mex_destroy(&c1_b_sfEvent);
  *(int32_T *)c1_outData = c1_y;
  sf_mex_destroy(&c1_mxArrayInData);
}

static uint8_T c1_d_emlrt_marshallIn(SFc1_ASV_pathplotInstanceStruct
  *chartInstance, const mxArray *c1_b_is_active_c1_ASV_pathplot, const char_T
  *c1_identifier)
{
  uint8_T c1_y;
  emlrtMsgIdentifier c1_thisId;
  c1_thisId.fIdentifier = c1_identifier;
  c1_thisId.fParent = NULL;
  c1_y = c1_e_emlrt_marshallIn(chartInstance, sf_mex_dup
    (c1_b_is_active_c1_ASV_pathplot), &c1_thisId);
  sf_mex_destroy(&c1_b_is_active_c1_ASV_pathplot);
  return c1_y;
}

static uint8_T c1_e_emlrt_marshallIn(SFc1_ASV_pathplotInstanceStruct
  *chartInstance, const mxArray *c1_u, const emlrtMsgIdentifier *c1_parentId)
{
  uint8_T c1_y;
  uint8_T c1_u0;
  sf_mex_import(c1_parentId, sf_mex_dup(c1_u), &c1_u0, 1, 3, 0U, 0, 0U, 0);
  c1_y = c1_u0;
  sf_mex_destroy(&c1_u);
  return c1_y;
}

static void init_dsm_address_info(SFc1_ASV_pathplotInstanceStruct *chartInstance)
{
}

/* SFunction Glue Code */
void sf_c1_ASV_pathplot_get_check_sum(mxArray *plhs[])
{
  ((real_T *)mxGetPr((plhs[0])))[0] = (real_T)(1984863861U);
  ((real_T *)mxGetPr((plhs[0])))[1] = (real_T)(927781964U);
  ((real_T *)mxGetPr((plhs[0])))[2] = (real_T)(3180669017U);
  ((real_T *)mxGetPr((plhs[0])))[3] = (real_T)(1175650606U);
}

mxArray *sf_c1_ASV_pathplot_get_autoinheritance_info(void)
{
  const char *autoinheritanceFields[] = { "checksum", "inputs", "parameters",
    "outputs", "locals" };

  mxArray *mxAutoinheritanceInfo = mxCreateStructMatrix(1,1,5,
    autoinheritanceFields);

  {
    mxArray *mxChecksum = mxCreateDoubleMatrix(4,1,mxREAL);
    double *pr = mxGetPr(mxChecksum);
    pr[0] = (double)(1913698968U);
    pr[1] = (double)(371430086U);
    pr[2] = (double)(861992978U);
    pr[3] = (double)(4148005143U);
    mxSetField(mxAutoinheritanceInfo,0,"checksum",mxChecksum);
  }

  {
    const char *dataFields[] = { "size", "type", "complexity" };

    mxArray *mxData = mxCreateStructMatrix(1,8,3,dataFields);

    {
      mxArray *mxSize = mxCreateDoubleMatrix(1,2,mxREAL);
      double *pr = mxGetPr(mxSize);
      pr[0] = (double)(1);
      pr[1] = (double)(1);
      mxSetField(mxData,0,"size",mxSize);
    }

    {
      const char *typeFields[] = { "base", "fixpt" };

      mxArray *mxType = mxCreateStructMatrix(1,1,2,typeFields);
      mxSetField(mxType,0,"base",mxCreateDoubleScalar(10));
      mxSetField(mxType,0,"fixpt",mxCreateDoubleMatrix(0,0,mxREAL));
      mxSetField(mxData,0,"type",mxType);
    }

    mxSetField(mxData,0,"complexity",mxCreateDoubleScalar(0));

    {
      mxArray *mxSize = mxCreateDoubleMatrix(1,2,mxREAL);
      double *pr = mxGetPr(mxSize);
      pr[0] = (double)(1);
      pr[1] = (double)(1);
      mxSetField(mxData,1,"size",mxSize);
    }

    {
      const char *typeFields[] = { "base", "fixpt" };

      mxArray *mxType = mxCreateStructMatrix(1,1,2,typeFields);
      mxSetField(mxType,0,"base",mxCreateDoubleScalar(10));
      mxSetField(mxType,0,"fixpt",mxCreateDoubleMatrix(0,0,mxREAL));
      mxSetField(mxData,1,"type",mxType);
    }

    mxSetField(mxData,1,"complexity",mxCreateDoubleScalar(0));

    {
      mxArray *mxSize = mxCreateDoubleMatrix(1,2,mxREAL);
      double *pr = mxGetPr(mxSize);
      pr[0] = (double)(1);
      pr[1] = (double)(1);
      mxSetField(mxData,2,"size",mxSize);
    }

    {
      const char *typeFields[] = { "base", "fixpt" };

      mxArray *mxType = mxCreateStructMatrix(1,1,2,typeFields);
      mxSetField(mxType,0,"base",mxCreateDoubleScalar(10));
      mxSetField(mxType,0,"fixpt",mxCreateDoubleMatrix(0,0,mxREAL));
      mxSetField(mxData,2,"type",mxType);
    }

    mxSetField(mxData,2,"complexity",mxCreateDoubleScalar(0));

    {
      mxArray *mxSize = mxCreateDoubleMatrix(1,2,mxREAL);
      double *pr = mxGetPr(mxSize);
      pr[0] = (double)(1);
      pr[1] = (double)(1);
      mxSetField(mxData,3,"size",mxSize);
    }

    {
      const char *typeFields[] = { "base", "fixpt" };

      mxArray *mxType = mxCreateStructMatrix(1,1,2,typeFields);
      mxSetField(mxType,0,"base",mxCreateDoubleScalar(10));
      mxSetField(mxType,0,"fixpt",mxCreateDoubleMatrix(0,0,mxREAL));
      mxSetField(mxData,3,"type",mxType);
    }

    mxSetField(mxData,3,"complexity",mxCreateDoubleScalar(0));

    {
      mxArray *mxSize = mxCreateDoubleMatrix(1,2,mxREAL);
      double *pr = mxGetPr(mxSize);
      pr[0] = (double)(1);
      pr[1] = (double)(1);
      mxSetField(mxData,4,"size",mxSize);
    }

    {
      const char *typeFields[] = { "base", "fixpt" };

      mxArray *mxType = mxCreateStructMatrix(1,1,2,typeFields);
      mxSetField(mxType,0,"base",mxCreateDoubleScalar(10));
      mxSetField(mxType,0,"fixpt",mxCreateDoubleMatrix(0,0,mxREAL));
      mxSetField(mxData,4,"type",mxType);
    }

    mxSetField(mxData,4,"complexity",mxCreateDoubleScalar(0));

    {
      mxArray *mxSize = mxCreateDoubleMatrix(1,2,mxREAL);
      double *pr = mxGetPr(mxSize);
      pr[0] = (double)(1);
      pr[1] = (double)(1);
      mxSetField(mxData,5,"size",mxSize);
    }

    {
      const char *typeFields[] = { "base", "fixpt" };

      mxArray *mxType = mxCreateStructMatrix(1,1,2,typeFields);
      mxSetField(mxType,0,"base",mxCreateDoubleScalar(10));
      mxSetField(mxType,0,"fixpt",mxCreateDoubleMatrix(0,0,mxREAL));
      mxSetField(mxData,5,"type",mxType);
    }

    mxSetField(mxData,5,"complexity",mxCreateDoubleScalar(0));

    {
      mxArray *mxSize = mxCreateDoubleMatrix(1,2,mxREAL);
      double *pr = mxGetPr(mxSize);
      pr[0] = (double)(1);
      pr[1] = (double)(1);
      mxSetField(mxData,6,"size",mxSize);
    }

    {
      const char *typeFields[] = { "base", "fixpt" };

      mxArray *mxType = mxCreateStructMatrix(1,1,2,typeFields);
      mxSetField(mxType,0,"base",mxCreateDoubleScalar(10));
      mxSetField(mxType,0,"fixpt",mxCreateDoubleMatrix(0,0,mxREAL));
      mxSetField(mxData,6,"type",mxType);
    }

    mxSetField(mxData,6,"complexity",mxCreateDoubleScalar(0));

    {
      mxArray *mxSize = mxCreateDoubleMatrix(1,2,mxREAL);
      double *pr = mxGetPr(mxSize);
      pr[0] = (double)(1);
      pr[1] = (double)(1);
      mxSetField(mxData,7,"size",mxSize);
    }

    {
      const char *typeFields[] = { "base", "fixpt" };

      mxArray *mxType = mxCreateStructMatrix(1,1,2,typeFields);
      mxSetField(mxType,0,"base",mxCreateDoubleScalar(10));
      mxSetField(mxType,0,"fixpt",mxCreateDoubleMatrix(0,0,mxREAL));
      mxSetField(mxData,7,"type",mxType);
    }

    mxSetField(mxData,7,"complexity",mxCreateDoubleScalar(0));
    mxSetField(mxAutoinheritanceInfo,0,"inputs",mxData);
  }

  {
    mxSetField(mxAutoinheritanceInfo,0,"parameters",mxCreateDoubleMatrix(0,0,
                mxREAL));
  }

  {
    const char *dataFields[] = { "size", "type", "complexity" };

    mxArray *mxData = mxCreateStructMatrix(1,8,3,dataFields);

    {
      mxArray *mxSize = mxCreateDoubleMatrix(1,2,mxREAL);
      double *pr = mxGetPr(mxSize);
      pr[0] = (double)(1);
      pr[1] = (double)(1);
      mxSetField(mxData,0,"size",mxSize);
    }

    {
      const char *typeFields[] = { "base", "fixpt" };

      mxArray *mxType = mxCreateStructMatrix(1,1,2,typeFields);
      mxSetField(mxType,0,"base",mxCreateDoubleScalar(10));
      mxSetField(mxType,0,"fixpt",mxCreateDoubleMatrix(0,0,mxREAL));
      mxSetField(mxData,0,"type",mxType);
    }

    mxSetField(mxData,0,"complexity",mxCreateDoubleScalar(0));

    {
      mxArray *mxSize = mxCreateDoubleMatrix(1,2,mxREAL);
      double *pr = mxGetPr(mxSize);
      pr[0] = (double)(1);
      pr[1] = (double)(1);
      mxSetField(mxData,1,"size",mxSize);
    }

    {
      const char *typeFields[] = { "base", "fixpt" };

      mxArray *mxType = mxCreateStructMatrix(1,1,2,typeFields);
      mxSetField(mxType,0,"base",mxCreateDoubleScalar(10));
      mxSetField(mxType,0,"fixpt",mxCreateDoubleMatrix(0,0,mxREAL));
      mxSetField(mxData,1,"type",mxType);
    }

    mxSetField(mxData,1,"complexity",mxCreateDoubleScalar(0));

    {
      mxArray *mxSize = mxCreateDoubleMatrix(1,2,mxREAL);
      double *pr = mxGetPr(mxSize);
      pr[0] = (double)(1);
      pr[1] = (double)(1);
      mxSetField(mxData,2,"size",mxSize);
    }

    {
      const char *typeFields[] = { "base", "fixpt" };

      mxArray *mxType = mxCreateStructMatrix(1,1,2,typeFields);
      mxSetField(mxType,0,"base",mxCreateDoubleScalar(10));
      mxSetField(mxType,0,"fixpt",mxCreateDoubleMatrix(0,0,mxREAL));
      mxSetField(mxData,2,"type",mxType);
    }

    mxSetField(mxData,2,"complexity",mxCreateDoubleScalar(0));

    {
      mxArray *mxSize = mxCreateDoubleMatrix(1,2,mxREAL);
      double *pr = mxGetPr(mxSize);
      pr[0] = (double)(1);
      pr[1] = (double)(1);
      mxSetField(mxData,3,"size",mxSize);
    }

    {
      const char *typeFields[] = { "base", "fixpt" };

      mxArray *mxType = mxCreateStructMatrix(1,1,2,typeFields);
      mxSetField(mxType,0,"base",mxCreateDoubleScalar(10));
      mxSetField(mxType,0,"fixpt",mxCreateDoubleMatrix(0,0,mxREAL));
      mxSetField(mxData,3,"type",mxType);
    }

    mxSetField(mxData,3,"complexity",mxCreateDoubleScalar(0));

    {
      mxArray *mxSize = mxCreateDoubleMatrix(1,2,mxREAL);
      double *pr = mxGetPr(mxSize);
      pr[0] = (double)(1);
      pr[1] = (double)(1);
      mxSetField(mxData,4,"size",mxSize);
    }

    {
      const char *typeFields[] = { "base", "fixpt" };

      mxArray *mxType = mxCreateStructMatrix(1,1,2,typeFields);
      mxSetField(mxType,0,"base",mxCreateDoubleScalar(10));
      mxSetField(mxType,0,"fixpt",mxCreateDoubleMatrix(0,0,mxREAL));
      mxSetField(mxData,4,"type",mxType);
    }

    mxSetField(mxData,4,"complexity",mxCreateDoubleScalar(0));

    {
      mxArray *mxSize = mxCreateDoubleMatrix(1,2,mxREAL);
      double *pr = mxGetPr(mxSize);
      pr[0] = (double)(1);
      pr[1] = (double)(1);
      mxSetField(mxData,5,"size",mxSize);
    }

    {
      const char *typeFields[] = { "base", "fixpt" };

      mxArray *mxType = mxCreateStructMatrix(1,1,2,typeFields);
      mxSetField(mxType,0,"base",mxCreateDoubleScalar(10));
      mxSetField(mxType,0,"fixpt",mxCreateDoubleMatrix(0,0,mxREAL));
      mxSetField(mxData,5,"type",mxType);
    }

    mxSetField(mxData,5,"complexity",mxCreateDoubleScalar(0));

    {
      mxArray *mxSize = mxCreateDoubleMatrix(1,2,mxREAL);
      double *pr = mxGetPr(mxSize);
      pr[0] = (double)(1);
      pr[1] = (double)(1);
      mxSetField(mxData,6,"size",mxSize);
    }

    {
      const char *typeFields[] = { "base", "fixpt" };

      mxArray *mxType = mxCreateStructMatrix(1,1,2,typeFields);
      mxSetField(mxType,0,"base",mxCreateDoubleScalar(10));
      mxSetField(mxType,0,"fixpt",mxCreateDoubleMatrix(0,0,mxREAL));
      mxSetField(mxData,6,"type",mxType);
    }

    mxSetField(mxData,6,"complexity",mxCreateDoubleScalar(0));

    {
      mxArray *mxSize = mxCreateDoubleMatrix(1,2,mxREAL);
      double *pr = mxGetPr(mxSize);
      pr[0] = (double)(1);
      pr[1] = (double)(1);
      mxSetField(mxData,7,"size",mxSize);
    }

    {
      const char *typeFields[] = { "base", "fixpt" };

      mxArray *mxType = mxCreateStructMatrix(1,1,2,typeFields);
      mxSetField(mxType,0,"base",mxCreateDoubleScalar(10));
      mxSetField(mxType,0,"fixpt",mxCreateDoubleMatrix(0,0,mxREAL));
      mxSetField(mxData,7,"type",mxType);
    }

    mxSetField(mxData,7,"complexity",mxCreateDoubleScalar(0));
    mxSetField(mxAutoinheritanceInfo,0,"outputs",mxData);
  }

  {
    mxSetField(mxAutoinheritanceInfo,0,"locals",mxCreateDoubleMatrix(0,0,mxREAL));
  }

  return(mxAutoinheritanceInfo);
}

static const mxArray *sf_get_sim_state_info_c1_ASV_pathplot(void)
{
  const char *infoFields[] = { "chartChecksum", "varInfo" };

  mxArray *mxInfo = mxCreateStructMatrix(1, 1, 2, infoFields);
  const char *infoEncStr[] = {
    "100 S1x9'type','srcId','name','auxInfo'{{M[1],M[14],T\"Drag_1\",},{M[1],M[15],T\"Drag_2\",},{M[1],M[17],T\"Drift_1\",},{M[1],M[19],T\"Drift_2\",},{M[1],M[16],T\"Push_1\",},{M[1],M[18],T\"Push_2\",},{M[1],M[5],T\"dot_S1\",},{M[1],M[11],T\"dot_S2\",},{M[8],M[0],T\"is_active_c1_ASV_pathplot\",}}"
  };

  mxArray *mxVarInfo = sf_mex_decode_encoded_mx_struct_array(infoEncStr, 9, 10);
  mxArray *mxChecksum = mxCreateDoubleMatrix(1, 4, mxREAL);
  sf_c1_ASV_pathplot_get_check_sum(&mxChecksum);
  mxSetField(mxInfo, 0, infoFields[0], mxChecksum);
  mxSetField(mxInfo, 0, infoFields[1], mxVarInfo);
  return mxInfo;
}

static void chart_debug_initialization(SimStruct *S, unsigned int
  fullDebuggerInitialization)
{
  if (!sim_mode_is_rtw_gen(S)) {
    SFc1_ASV_pathplotInstanceStruct *chartInstance;
    chartInstance = (SFc1_ASV_pathplotInstanceStruct *) ((ChartInfoStruct *)
      (ssGetUserData(S)))->chartInstance;
    if (ssIsFirstInitCond(S) && fullDebuggerInitialization==1) {
      /* do this only if simulation is starting */
      {
        unsigned int chartAlreadyPresent;
        chartAlreadyPresent = sf_debug_initialize_chart
          (_ASV_pathplotMachineNumber_,
           1,
           1,
           1,
           16,
           0,
           0,
           0,
           0,
           0,
           &(chartInstance->chartNumber),
           &(chartInstance->instanceNumber),
           ssGetPath(S),
           (void *)S);
        if (chartAlreadyPresent==0) {
          /* this is the first instance */
          init_script_number_translation(_ASV_pathplotMachineNumber_,
            chartInstance->chartNumber);
          sf_debug_set_chart_disable_implicit_casting
            (_ASV_pathplotMachineNumber_,chartInstance->chartNumber,1);
          sf_debug_set_chart_event_thresholds(_ASV_pathplotMachineNumber_,
            chartInstance->chartNumber,
            0,
            0,
            0);
          _SFD_SET_DATA_PROPS(0,1,1,0,"Rho");
          _SFD_SET_DATA_PROPS(1,2,0,1,"dot_S1");
          _SFD_SET_DATA_PROPS(2,1,1,0,"S1");
          _SFD_SET_DATA_PROPS(3,1,1,0,"S2");
          _SFD_SET_DATA_PROPS(4,1,1,0,"Theta");
          _SFD_SET_DATA_PROPS(5,1,1,0,"Length");
          _SFD_SET_DATA_PROPS(6,1,1,0,"Width");
          _SFD_SET_DATA_PROPS(7,2,0,1,"dot_S2");
          _SFD_SET_DATA_PROPS(8,2,0,1,"Push_1");
          _SFD_SET_DATA_PROPS(9,1,1,0,"RPM1");
          _SFD_SET_DATA_PROPS(10,1,1,0,"RPM2");
          _SFD_SET_DATA_PROPS(11,2,0,1,"Drag_1");
          _SFD_SET_DATA_PROPS(12,2,0,1,"Drift_1");
          _SFD_SET_DATA_PROPS(13,2,0,1,"Push_2");
          _SFD_SET_DATA_PROPS(14,2,0,1,"Drag_2");
          _SFD_SET_DATA_PROPS(15,2,0,1,"Drift_2");
          _SFD_STATE_INFO(0,0,2);
          _SFD_CH_SUBSTATE_COUNT(0);
          _SFD_CH_SUBSTATE_DECOMP(0);
        }

        _SFD_CV_INIT_CHART(0,0,0,0);

        {
          _SFD_CV_INIT_STATE(0,0,0,0,0,0,NULL,NULL);
        }

        _SFD_CV_INIT_TRANS(0,0,NULL,NULL,0,NULL);

        /* Initialization of MATLAB Function Model Coverage */
        _SFD_CV_INIT_EML(0,1,0,0,0,0,0,0,0);
        _SFD_CV_INIT_EML_FCN(0,0,"eML_blk_kernel",0,-1,523);
        _SFD_TRANS_COV_WTS(0,0,0,1,0);
        if (chartAlreadyPresent==0) {
          _SFD_TRANS_COV_MAPS(0,
                              0,NULL,NULL,
                              0,NULL,NULL,
                              1,NULL,NULL,
                              0,NULL,NULL);
        }

        _SFD_SET_DATA_COMPILED_PROPS(0,SF_DOUBLE,0,NULL,0,0,0,0.0,1.0,0,0,
          (MexFcnForType)c1_sf_marshallOut,(MexInFcnForType)NULL);
        _SFD_SET_DATA_COMPILED_PROPS(1,SF_DOUBLE,0,NULL,0,0,0,0.0,1.0,0,0,
          (MexFcnForType)c1_sf_marshallOut,(MexInFcnForType)c1_sf_marshallIn);
        _SFD_SET_DATA_COMPILED_PROPS(2,SF_DOUBLE,0,NULL,0,0,0,0.0,1.0,0,0,
          (MexFcnForType)c1_sf_marshallOut,(MexInFcnForType)NULL);
        _SFD_SET_DATA_COMPILED_PROPS(3,SF_DOUBLE,0,NULL,0,0,0,0.0,1.0,0,0,
          (MexFcnForType)c1_sf_marshallOut,(MexInFcnForType)NULL);
        _SFD_SET_DATA_COMPILED_PROPS(4,SF_DOUBLE,0,NULL,0,0,0,0.0,1.0,0,0,
          (MexFcnForType)c1_sf_marshallOut,(MexInFcnForType)NULL);
        _SFD_SET_DATA_COMPILED_PROPS(5,SF_DOUBLE,0,NULL,0,0,0,0.0,1.0,0,0,
          (MexFcnForType)c1_sf_marshallOut,(MexInFcnForType)NULL);
        _SFD_SET_DATA_COMPILED_PROPS(6,SF_DOUBLE,0,NULL,0,0,0,0.0,1.0,0,0,
          (MexFcnForType)c1_sf_marshallOut,(MexInFcnForType)NULL);
        _SFD_SET_DATA_COMPILED_PROPS(7,SF_DOUBLE,0,NULL,0,0,0,0.0,1.0,0,0,
          (MexFcnForType)c1_sf_marshallOut,(MexInFcnForType)c1_sf_marshallIn);
        _SFD_SET_DATA_COMPILED_PROPS(8,SF_DOUBLE,0,NULL,0,0,0,0.0,1.0,0,0,
          (MexFcnForType)c1_sf_marshallOut,(MexInFcnForType)c1_sf_marshallIn);
        _SFD_SET_DATA_COMPILED_PROPS(9,SF_DOUBLE,0,NULL,0,0,0,0.0,1.0,0,0,
          (MexFcnForType)c1_sf_marshallOut,(MexInFcnForType)NULL);
        _SFD_SET_DATA_COMPILED_PROPS(10,SF_DOUBLE,0,NULL,0,0,0,0.0,1.0,0,0,
          (MexFcnForType)c1_sf_marshallOut,(MexInFcnForType)NULL);
        _SFD_SET_DATA_COMPILED_PROPS(11,SF_DOUBLE,0,NULL,0,0,0,0.0,1.0,0,0,
          (MexFcnForType)c1_sf_marshallOut,(MexInFcnForType)c1_sf_marshallIn);
        _SFD_SET_DATA_COMPILED_PROPS(12,SF_DOUBLE,0,NULL,0,0,0,0.0,1.0,0,0,
          (MexFcnForType)c1_sf_marshallOut,(MexInFcnForType)c1_sf_marshallIn);
        _SFD_SET_DATA_COMPILED_PROPS(13,SF_DOUBLE,0,NULL,0,0,0,0.0,1.0,0,0,
          (MexFcnForType)c1_sf_marshallOut,(MexInFcnForType)c1_sf_marshallIn);
        _SFD_SET_DATA_COMPILED_PROPS(14,SF_DOUBLE,0,NULL,0,0,0,0.0,1.0,0,0,
          (MexFcnForType)c1_sf_marshallOut,(MexInFcnForType)c1_sf_marshallIn);
        _SFD_SET_DATA_COMPILED_PROPS(15,SF_DOUBLE,0,NULL,0,0,0,0.0,1.0,0,0,
          (MexFcnForType)c1_sf_marshallOut,(MexInFcnForType)c1_sf_marshallIn);

        {
          real_T *c1_Rho;
          real_T *c1_dot_S1;
          real_T *c1_S1;
          real_T *c1_S2;
          real_T *c1_Theta;
          real_T *c1_Length;
          real_T *c1_Width;
          real_T *c1_dot_S2;
          real_T *c1_Push_1;
          real_T *c1_RPM1;
          real_T *c1_RPM2;
          real_T *c1_Drag_1;
          real_T *c1_Drift_1;
          real_T *c1_Push_2;
          real_T *c1_Drag_2;
          real_T *c1_Drift_2;
          c1_Drift_2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 8);
          c1_Drag_2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 7);
          c1_Push_2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 6);
          c1_Drift_1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 5);
          c1_Drag_1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 4);
          c1_RPM2 = (real_T *)ssGetInputPortSignal(chartInstance->S, 7);
          c1_RPM1 = (real_T *)ssGetInputPortSignal(chartInstance->S, 6);
          c1_Push_1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 3);
          c1_dot_S2 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 2);
          c1_Width = (real_T *)ssGetInputPortSignal(chartInstance->S, 5);
          c1_Length = (real_T *)ssGetInputPortSignal(chartInstance->S, 4);
          c1_Theta = (real_T *)ssGetInputPortSignal(chartInstance->S, 3);
          c1_S2 = (real_T *)ssGetInputPortSignal(chartInstance->S, 2);
          c1_S1 = (real_T *)ssGetInputPortSignal(chartInstance->S, 1);
          c1_dot_S1 = (real_T *)ssGetOutputPortSignal(chartInstance->S, 1);
          c1_Rho = (real_T *)ssGetInputPortSignal(chartInstance->S, 0);
          _SFD_SET_DATA_VALUE_PTR(0U, c1_Rho);
          _SFD_SET_DATA_VALUE_PTR(1U, c1_dot_S1);
          _SFD_SET_DATA_VALUE_PTR(2U, c1_S1);
          _SFD_SET_DATA_VALUE_PTR(3U, c1_S2);
          _SFD_SET_DATA_VALUE_PTR(4U, c1_Theta);
          _SFD_SET_DATA_VALUE_PTR(5U, c1_Length);
          _SFD_SET_DATA_VALUE_PTR(6U, c1_Width);
          _SFD_SET_DATA_VALUE_PTR(7U, c1_dot_S2);
          _SFD_SET_DATA_VALUE_PTR(8U, c1_Push_1);
          _SFD_SET_DATA_VALUE_PTR(9U, c1_RPM1);
          _SFD_SET_DATA_VALUE_PTR(10U, c1_RPM2);
          _SFD_SET_DATA_VALUE_PTR(11U, c1_Drag_1);
          _SFD_SET_DATA_VALUE_PTR(12U, c1_Drift_1);
          _SFD_SET_DATA_VALUE_PTR(13U, c1_Push_2);
          _SFD_SET_DATA_VALUE_PTR(14U, c1_Drag_2);
          _SFD_SET_DATA_VALUE_PTR(15U, c1_Drift_2);
        }
      }
    } else {
      sf_debug_reset_current_state_configuration(_ASV_pathplotMachineNumber_,
        chartInstance->chartNumber,chartInstance->instanceNumber);
    }
  }
}

static void sf_opaque_initialize_c1_ASV_pathplot(void *chartInstanceVar)
{
  chart_debug_initialization(((SFc1_ASV_pathplotInstanceStruct*)
    chartInstanceVar)->S,0);
  initialize_params_c1_ASV_pathplot((SFc1_ASV_pathplotInstanceStruct*)
    chartInstanceVar);
  initialize_c1_ASV_pathplot((SFc1_ASV_pathplotInstanceStruct*) chartInstanceVar);
}

static void sf_opaque_enable_c1_ASV_pathplot(void *chartInstanceVar)
{
  enable_c1_ASV_pathplot((SFc1_ASV_pathplotInstanceStruct*) chartInstanceVar);
}

static void sf_opaque_disable_c1_ASV_pathplot(void *chartInstanceVar)
{
  disable_c1_ASV_pathplot((SFc1_ASV_pathplotInstanceStruct*) chartInstanceVar);
}

static void sf_opaque_gateway_c1_ASV_pathplot(void *chartInstanceVar)
{
  sf_c1_ASV_pathplot((SFc1_ASV_pathplotInstanceStruct*) chartInstanceVar);
}

extern const mxArray* sf_internal_get_sim_state_c1_ASV_pathplot(SimStruct* S)
{
  ChartInfoStruct *chartInfo = (ChartInfoStruct*) ssGetUserData(S);
  mxArray *plhs[1] = { NULL };

  mxArray *prhs[4];
  int mxError = 0;
  prhs[0] = mxCreateString("chart_simctx_raw2high");
  prhs[1] = mxCreateDoubleScalar(ssGetSFuncBlockHandle(S));
  prhs[2] = (mxArray*) get_sim_state_c1_ASV_pathplot
    ((SFc1_ASV_pathplotInstanceStruct*)chartInfo->chartInstance);/* raw sim ctx */
  prhs[3] = (mxArray*) sf_get_sim_state_info_c1_ASV_pathplot();/* state var info */
  mxError = sf_mex_call_matlab(1, plhs, 4, prhs, "sfprivate");
  mxDestroyArray(prhs[0]);
  mxDestroyArray(prhs[1]);
  mxDestroyArray(prhs[2]);
  mxDestroyArray(prhs[3]);
  if (mxError || plhs[0] == NULL) {
    sf_mex_error_message("Stateflow Internal Error: \nError calling 'chart_simctx_raw2high'.\n");
  }

  return plhs[0];
}

extern void sf_internal_set_sim_state_c1_ASV_pathplot(SimStruct* S, const
  mxArray *st)
{
  ChartInfoStruct *chartInfo = (ChartInfoStruct*) ssGetUserData(S);
  mxArray *plhs[1] = { NULL };

  mxArray *prhs[4];
  int mxError = 0;
  prhs[0] = mxCreateString("chart_simctx_high2raw");
  prhs[1] = mxCreateDoubleScalar(ssGetSFuncBlockHandle(S));
  prhs[2] = mxDuplicateArray(st);      /* high level simctx */
  prhs[3] = (mxArray*) sf_get_sim_state_info_c1_ASV_pathplot();/* state var info */
  mxError = sf_mex_call_matlab(1, plhs, 4, prhs, "sfprivate");
  mxDestroyArray(prhs[0]);
  mxDestroyArray(prhs[1]);
  mxDestroyArray(prhs[2]);
  mxDestroyArray(prhs[3]);
  if (mxError || plhs[0] == NULL) {
    sf_mex_error_message("Stateflow Internal Error: \nError calling 'chart_simctx_high2raw'.\n");
  }

  set_sim_state_c1_ASV_pathplot((SFc1_ASV_pathplotInstanceStruct*)
    chartInfo->chartInstance, mxDuplicateArray(plhs[0]));
  mxDestroyArray(plhs[0]);
}

static const mxArray* sf_opaque_get_sim_state_c1_ASV_pathplot(SimStruct* S)
{
  return sf_internal_get_sim_state_c1_ASV_pathplot(S);
}

static void sf_opaque_set_sim_state_c1_ASV_pathplot(SimStruct* S, const mxArray *
  st)
{
  sf_internal_set_sim_state_c1_ASV_pathplot(S, st);
}

static void sf_opaque_terminate_c1_ASV_pathplot(void *chartInstanceVar)
{
  if (chartInstanceVar!=NULL) {
    SimStruct *S = ((SFc1_ASV_pathplotInstanceStruct*) chartInstanceVar)->S;
    if (sim_mode_is_rtw_gen(S) || sim_mode_is_external(S)) {
      sf_clear_rtw_identifier(S);
    }

    finalize_c1_ASV_pathplot((SFc1_ASV_pathplotInstanceStruct*) chartInstanceVar);
    free((void *)chartInstanceVar);
    ssSetUserData(S,NULL);
  }
}

static void sf_opaque_init_subchart_simstructs(void *chartInstanceVar)
{
  initSimStructsc1_ASV_pathplot((SFc1_ASV_pathplotInstanceStruct*)
    chartInstanceVar);
}

extern unsigned int sf_machine_global_initializer_called(void);
static void mdlProcessParameters_c1_ASV_pathplot(SimStruct *S)
{
  int i;
  for (i=0;i<ssGetNumRunTimeParams(S);i++) {
    if (ssGetSFcnParamTunable(S,i)) {
      ssUpdateDlgParamAsRunTimeParam(S,i);
    }
  }

  if (sf_machine_global_initializer_called()) {
    initialize_params_c1_ASV_pathplot((SFc1_ASV_pathplotInstanceStruct*)
      (((ChartInfoStruct *)ssGetUserData(S))->chartInstance));
  }
}

static void mdlSetWorkWidths_c1_ASV_pathplot(SimStruct *S)
{
  if (sim_mode_is_rtw_gen(S) || sim_mode_is_external(S)) {
    int_T chartIsInlinable =
      (int_T)sf_is_chart_inlinable(S,"ASV_pathplot","ASV_pathplot",1);
    ssSetStateflowIsInlinable(S,chartIsInlinable);
    ssSetRTWCG(S,sf_rtw_info_uint_prop(S,"ASV_pathplot","ASV_pathplot",1,"RTWCG"));
    ssSetEnableFcnIsTrivial(S,1);
    ssSetDisableFcnIsTrivial(S,1);
    ssSetNotMultipleInlinable(S,sf_rtw_info_uint_prop(S,"ASV_pathplot",
      "ASV_pathplot",1,"gatewayCannotBeInlinedMultipleTimes"));
    if (chartIsInlinable) {
      ssSetInputPortOptimOpts(S, 0, SS_REUSABLE_AND_LOCAL);
      ssSetInputPortOptimOpts(S, 1, SS_REUSABLE_AND_LOCAL);
      ssSetInputPortOptimOpts(S, 2, SS_REUSABLE_AND_LOCAL);
      ssSetInputPortOptimOpts(S, 3, SS_REUSABLE_AND_LOCAL);
      ssSetInputPortOptimOpts(S, 4, SS_REUSABLE_AND_LOCAL);
      ssSetInputPortOptimOpts(S, 5, SS_REUSABLE_AND_LOCAL);
      ssSetInputPortOptimOpts(S, 6, SS_REUSABLE_AND_LOCAL);
      ssSetInputPortOptimOpts(S, 7, SS_REUSABLE_AND_LOCAL);
      sf_mark_chart_expressionable_inputs(S,"ASV_pathplot","ASV_pathplot",1,8);
      sf_mark_chart_reusable_outputs(S,"ASV_pathplot","ASV_pathplot",1,8);
    }

    sf_set_rtw_dwork_info(S,"ASV_pathplot","ASV_pathplot",1);
    ssSetHasSubFunctions(S,!(chartIsInlinable));
  } else {
  }

  ssSetOptions(S,ssGetOptions(S)|SS_OPTION_WORKS_WITH_CODE_REUSE);
  ssSetChecksum0(S,(4005864978U));
  ssSetChecksum1(S,(2956297971U));
  ssSetChecksum2(S,(2071769975U));
  ssSetChecksum3(S,(2273888319U));
  ssSetmdlDerivatives(S, NULL);
  ssSetExplicitFCSSCtrl(S,1);
}

static void mdlRTW_c1_ASV_pathplot(SimStruct *S)
{
  if (sim_mode_is_rtw_gen(S)) {
    sf_write_symbol_mapping(S, "ASV_pathplot", "ASV_pathplot",1);
    ssWriteRTWStrParam(S, "StateflowChartType", "Embedded MATLAB");
  }
}

static void mdlStart_c1_ASV_pathplot(SimStruct *S)
{
  SFc1_ASV_pathplotInstanceStruct *chartInstance;
  chartInstance = (SFc1_ASV_pathplotInstanceStruct *)malloc(sizeof
    (SFc1_ASV_pathplotInstanceStruct));
  memset(chartInstance, 0, sizeof(SFc1_ASV_pathplotInstanceStruct));
  if (chartInstance==NULL) {
    sf_mex_error_message("Could not allocate memory for chart instance.");
  }

  chartInstance->chartInfo.chartInstance = chartInstance;
  chartInstance->chartInfo.isEMLChart = 1;
  chartInstance->chartInfo.chartInitialized = 0;
  chartInstance->chartInfo.sFunctionGateway = sf_opaque_gateway_c1_ASV_pathplot;
  chartInstance->chartInfo.initializeChart =
    sf_opaque_initialize_c1_ASV_pathplot;
  chartInstance->chartInfo.terminateChart = sf_opaque_terminate_c1_ASV_pathplot;
  chartInstance->chartInfo.enableChart = sf_opaque_enable_c1_ASV_pathplot;
  chartInstance->chartInfo.disableChart = sf_opaque_disable_c1_ASV_pathplot;
  chartInstance->chartInfo.getSimState = sf_opaque_get_sim_state_c1_ASV_pathplot;
  chartInstance->chartInfo.setSimState = sf_opaque_set_sim_state_c1_ASV_pathplot;
  chartInstance->chartInfo.getSimStateInfo =
    sf_get_sim_state_info_c1_ASV_pathplot;
  chartInstance->chartInfo.zeroCrossings = NULL;
  chartInstance->chartInfo.outputs = NULL;
  chartInstance->chartInfo.derivatives = NULL;
  chartInstance->chartInfo.mdlRTW = mdlRTW_c1_ASV_pathplot;
  chartInstance->chartInfo.mdlStart = mdlStart_c1_ASV_pathplot;
  chartInstance->chartInfo.mdlSetWorkWidths = mdlSetWorkWidths_c1_ASV_pathplot;
  chartInstance->chartInfo.extModeExec = NULL;
  chartInstance->chartInfo.restoreLastMajorStepConfiguration = NULL;
  chartInstance->chartInfo.restoreBeforeLastMajorStepConfiguration = NULL;
  chartInstance->chartInfo.storeCurrentConfiguration = NULL;
  chartInstance->S = S;
  ssSetUserData(S,(void *)(&(chartInstance->chartInfo)));/* register the chart instance with simstruct */
  init_dsm_address_info(chartInstance);
  if (!sim_mode_is_rtw_gen(S)) {
  }

  sf_opaque_init_subchart_simstructs(chartInstance->chartInfo.chartInstance);
  chart_debug_initialization(S,1);
}

void c1_ASV_pathplot_method_dispatcher(SimStruct *S, int_T method, void *data)
{
  switch (method) {
   case SS_CALL_MDL_START:
    mdlStart_c1_ASV_pathplot(S);
    break;

   case SS_CALL_MDL_SET_WORK_WIDTHS:
    mdlSetWorkWidths_c1_ASV_pathplot(S);
    break;

   case SS_CALL_MDL_PROCESS_PARAMETERS:
    mdlProcessParameters_c1_ASV_pathplot(S);
    break;

   default:
    /* Unhandled method */
    sf_mex_error_message("Stateflow Internal Error:\n"
                         "Error calling c1_ASV_pathplot_method_dispatcher.\n"
                         "Can't handle method %d.\n", method);
    break;
  }
}
