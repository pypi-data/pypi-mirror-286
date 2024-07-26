from typing import List

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ..........Internal.Types import DataType
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardDevCls:
	"""StandardDev commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("standardDev", core, parent)

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST[:CC<Carrier>]:MODulation:PERRor:DMRS:LOW:SDEViation \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.listPy.cc.modulation.perror.dmrs.low.standardDev.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Return phase error DMRS values for low and high EVM window position, for all measured list mode segments, for carrier <c>.
		The values described below are returned by FETCh commands. CALCulate commands return limit check results instead, one
		value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: ph_error_dmrs_low: Comma-separated list of values, one per measured segment"""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:CC{carrierComponent_cmd_val}:MODulation:PERRor:DMRS:LOW:SDEViation?', suppressed)
		return response
