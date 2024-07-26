from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ListPyCls:
	"""ListPy commands group definition. 17 total commands, 3 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("listPy", core, parent)

	@property
	def lrange(self):
		"""lrange commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lrange'):
			from .Lrange import LrangeCls
			self._lrange = LrangeCls(self._core, self._cmd_group)
		return self._lrange

	@property
	def segment(self):
		"""segment commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_segment'):
			from .Segment import SegmentCls
			self._segment = SegmentCls(self._core, self._cmd_group)
		return self._segment

	@property
	def singleCmw(self):
		"""singleCmw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_singleCmw'):
			from .SingleCmw import SingleCmwCls
			self._singleCmw = SingleCmwCls(self._core, self._cmd_group)
		return self._singleCmw

	def get_os_index(self) -> int or bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:OSINdex \n
		Snippet: value: int or bool = driver.configure.nrSubMeas.multiEval.listPy.get_os_index() \n
		No command help available \n
			:return: offline_seg_index: (integer or boolean) No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:OSINdex?')
		return Conversions.str_to_int_or_bool(response)

	def set_os_index(self, offline_seg_index: int or bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:OSINdex \n
		Snippet: driver.configure.nrSubMeas.multiEval.listPy.set_os_index(offline_seg_index = 1) \n
		No command help available \n
			:param offline_seg_index: (integer or boolean) No help available
		"""
		param = Conversions.decimal_or_bool_value_to_str(offline_seg_index)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:OSINdex {param}')

	# noinspection PyTypeChecker
	def get_cmode(self) -> enums.ParameterSetMode:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:CMODe \n
		Snippet: value: enums.ParameterSetMode = driver.configure.nrSubMeas.multiEval.listPy.get_cmode() \n
		No command help available \n
			:return: connector_mode: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:CMODe?')
		return Conversions.str_to_scalar_enum(response, enums.ParameterSetMode)

	def set_cmode(self, connector_mode: enums.ParameterSetMode) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:CMODe \n
		Snippet: driver.configure.nrSubMeas.multiEval.listPy.set_cmode(connector_mode = enums.ParameterSetMode.GLOBal) \n
		No command help available \n
			:param connector_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(connector_mode, enums.ParameterSetMode)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:CMODe {param}')

	def get_nconnections(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:NCONnections \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.listPy.get_nconnections() \n
		No command help available \n
			:return: no_of_connections: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:NCONnections?')
		return Conversions.str_to_int(response)

	def set_nconnections(self, no_of_connections: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:NCONnections \n
		Snippet: driver.configure.nrSubMeas.multiEval.listPy.set_nconnections(no_of_connections = 1) \n
		No command help available \n
			:param no_of_connections: No help available
		"""
		param = Conversions.decimal_value_to_str(no_of_connections)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:NCONnections {param}')

	def get_value(self) -> bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST \n
		Snippet: value: bool = driver.configure.nrSubMeas.multiEval.listPy.get_value() \n
		Enables or disables the list mode. \n
			:return: enable: OFF: Disable list mode. ON: Enable list mode.
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST?')
		return Conversions.str_to_bool(response)

	def set_value(self, enable: bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST \n
		Snippet: driver.configure.nrSubMeas.multiEval.listPy.set_value(enable = False) \n
		Enables or disables the list mode. \n
			:param enable: OFF: Disable list mode. ON: Enable list mode.
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST {param}')

	def clone(self) -> 'ListPyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ListPyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
