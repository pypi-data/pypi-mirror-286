from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardDevCls:
	"""StandardDev commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("standardDev", core, parent)

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default, minRange=repcap.MinRange.Default) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST[:CC<Carrier>]:ESFLatness:MINR<nr6g>:SDEViation \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.listPy.cc.esFlatness.minr.standardDev.fetch(carrierComponent = repcap.CarrierComponent.Default, minRange = repcap.MinRange.Default) \n
		Return equalizer spectrum flatness single value results (minimum within a range) for all measured list mode segments, for
		carrier <c>. The values described below are returned by FETCh commands. CALCulate commands return limit check results
		instead, one value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param minRange: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Minr')
			:return: minr: Comma-separated list of values, one per measured segment."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		minRange_cmd_val = self._cmd_group.get_repcap_cmd_value(minRange, repcap.MinRange)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:CC{carrierComponent_cmd_val}:ESFLatness:MINR{minRange_cmd_val}:SDEViation?', suppressed)
		return response
