from typing import List

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ..........Internal.Types import DataType
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExtremeCls:
	"""Extreme commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("extreme", core, parent)

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST[:CC<Carrier>]:MODulation:PERRor:PEAK:LOW:EXTReme \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.listPy.cc.modulation.perror.peak.low.extreme.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Return phase error peak values for low and high EVM window position, for all measured list mode segments, for carrier <c>.
		The values described below are returned by FETCh commands. CALCulate commands return limit check results instead, one
		value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: ph_error_peak_low: Comma-separated list of values, one per measured segment"""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:CC{carrierComponent_cmd_val}:MODulation:PERRor:PEAK:LOW:EXTReme?', suppressed)
		return response

	def calculate(self, carrierComponent=repcap.CarrierComponent.Default) -> List[float or bool]:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST[:CC<Carrier>]:MODulation:PERRor:PEAK:LOW:EXTReme \n
		Snippet: value: List[float or bool] = driver.nrSubMeas.multiEval.listPy.cc.modulation.perror.peak.low.extreme.calculate(carrierComponent = repcap.CarrierComponent.Default) \n
		Return phase error peak values for low and high EVM window position, for all measured list mode segments, for carrier <c>.
		The values described below are returned by FETCh commands. CALCulate commands return limit check results instead, one
		value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: ph_error_peak_low: (float or boolean items) Comma-separated list of values, one per measured segment"""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:CC{carrierComponent_cmd_val}:MODulation:PERRor:PEAK:LOW:EXTReme?', suppressed)
		return Conversions.str_to_float_or_bool_list(response)
