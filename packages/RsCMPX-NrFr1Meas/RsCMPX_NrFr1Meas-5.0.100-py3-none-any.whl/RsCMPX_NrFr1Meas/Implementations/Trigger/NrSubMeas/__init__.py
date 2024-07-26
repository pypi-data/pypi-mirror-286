from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NrSubMeasCls:
	"""NrSubMeas commands group definition. 23 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nrSubMeas", core, parent)

	@property
	def multiEval(self):
		"""multiEval commands group. 1 Sub-classes, 8 commands."""
		if not hasattr(self, '_multiEval'):
			from .MultiEval import MultiEvalCls
			self._multiEval = MultiEvalCls(self._core, self._cmd_group)
		return self._multiEval

	@property
	def listPy(self):
		"""listPy commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_listPy'):
			from .ListPy import ListPyCls
			self._listPy = ListPyCls(self._core, self._cmd_group)
		return self._listPy

	@property
	def prach(self):
		"""prach commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_prach'):
			from .Prach import PrachCls
			self._prach = PrachCls(self._core, self._cmd_group)
		return self._prach

	@property
	def srs(self):
		"""srs commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_srs'):
			from .Srs import SrsCls
			self._srs = SrsCls(self._core, self._cmd_group)
		return self._srs

	@property
	def tpc(self):
		"""tpc commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_tpc'):
			from .Tpc import TpcCls
			self._tpc = TpcCls(self._core, self._cmd_group)
		return self._tpc

	def clone(self) -> 'NrSubMeasCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NrSubMeasCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
