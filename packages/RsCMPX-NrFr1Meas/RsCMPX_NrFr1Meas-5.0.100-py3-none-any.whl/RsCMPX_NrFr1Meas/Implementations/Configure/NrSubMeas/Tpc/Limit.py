from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LimitCls:
	"""Limit commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("limit", core, parent)

	def get_ttolerance(self) -> float:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:TPC:LIMit:TTOLerance \n
		Snippet: value: float = driver.configure.nrSubMeas.tpc.limit.get_ttolerance() \n
		No command help available \n
			:return: test_tolerance: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:TPC:LIMit:TTOLerance?')
		return Conversions.str_to_float(response)

	def set_ttolerance(self, test_tolerance: float) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:TPC:LIMit:TTOLerance \n
		Snippet: driver.configure.nrSubMeas.tpc.limit.set_ttolerance(test_tolerance = 1.0) \n
		No command help available \n
			:param test_tolerance: No help available
		"""
		param = Conversions.decimal_value_to_str(test_tolerance)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:TPC:LIMit:TTOLerance {param}')
