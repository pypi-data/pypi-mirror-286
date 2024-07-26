from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MaximumCls:
	"""Maximum commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("maximum", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEMask:TXPower:MAXimum \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.listPy.seMask.txPower.maximum.fetch() \n
		Return the total TX power in the slot for all measured list mode segments. The values described below are returned by
		FETCh commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:return: tx_power: Comma-separated list of values, one per measured segment"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEMask:TXPower:MAXimum?', suppressed)
		return response

	def calculate(self) -> List[float or bool]:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:SEMask:TXPower:MAXimum \n
		Snippet: value: List[float or bool] = driver.nrSubMeas.multiEval.listPy.seMask.txPower.maximum.calculate() \n
		Return the total TX power in the slot for all measured list mode segments. The values described below are returned by
		FETCh commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
		Suppressed linked return values: reliability \n
			:return: tx_power: (float or boolean items) Comma-separated list of values, one per measured segment"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:SEMask:TXPower:MAXimum?', suppressed)
		return Conversions.str_to_float_or_bool_list(response)
