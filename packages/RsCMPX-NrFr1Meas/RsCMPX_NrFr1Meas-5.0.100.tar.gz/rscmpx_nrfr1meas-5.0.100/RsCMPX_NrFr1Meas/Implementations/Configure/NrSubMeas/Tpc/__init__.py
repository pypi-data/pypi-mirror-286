from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TpcCls:
	"""Tpc commands group definition. 5 total commands, 1 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tpc", core, parent)

	@property
	def limit(self):
		"""limit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_limit'):
			from .Limit import LimitCls
			self._limit = LimitCls(self._core, self._cmd_group)
		return self._limit

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:TPC:TOUT \n
		Snippet: value: float = driver.configure.nrSubMeas.tpc.get_timeout() \n
		No command help available \n
			:return: timeout: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:TPC:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, timeout: float) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:TPC:TOUT \n
		Snippet: driver.configure.nrSubMeas.tpc.set_timeout(timeout = 1.0) \n
		No command help available \n
			:param timeout: No help available
		"""
		param = Conversions.decimal_value_to_str(timeout)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:TPC:TOUT {param}')

	# noinspection PyTypeChecker
	def get_direction(self) -> enums.Direction:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:TPC:DIRection \n
		Snippet: value: enums.Direction = driver.configure.nrSubMeas.tpc.get_direction() \n
		No command help available \n
			:return: direction: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:TPC:DIRection?')
		return Conversions.str_to_scalar_enum(response, enums.Direction)

	def set_direction(self, direction: enums.Direction) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:TPC:DIRection \n
		Snippet: driver.configure.nrSubMeas.tpc.set_direction(direction = enums.Direction.ALTernating) \n
		No command help available \n
			:param direction: No help available
		"""
		param = Conversions.enum_scalar_to_str(direction, enums.Direction)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:TPC:DIRection {param}')

	def get_st_id(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:TPC:STID \n
		Snippet: value: int = driver.configure.nrSubMeas.tpc.get_st_id() \n
		No command help available \n
			:return: sub_test_id: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:TPC:STID?')
		return Conversions.str_to_int(response)

	def set_st_id(self, sub_test_id: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:TPC:STID \n
		Snippet: driver.configure.nrSubMeas.tpc.set_st_id(sub_test_id = 1) \n
		No command help available \n
			:param sub_test_id: No help available
		"""
		param = Conversions.decimal_value_to_str(sub_test_id)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:TPC:STID {param}')

	# noinspection PyTypeChecker
	def get_pattern(self) -> enums.Pattern:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:TPC:PATTern \n
		Snippet: value: enums.Pattern = driver.configure.nrSubMeas.tpc.get_pattern() \n
		No command help available \n
			:return: pattern: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:TPC:PATTern?')
		return Conversions.str_to_scalar_enum(response, enums.Pattern)

	def set_pattern(self, pattern: enums.Pattern) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:TPC:PATTern \n
		Snippet: driver.configure.nrSubMeas.tpc.set_pattern(pattern = enums.Pattern.A) \n
		No command help available \n
			:param pattern: No help available
		"""
		param = Conversions.enum_scalar_to_str(pattern, enums.Pattern)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:TPC:PATTern {param}')

	def clone(self) -> 'TpcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TpcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
