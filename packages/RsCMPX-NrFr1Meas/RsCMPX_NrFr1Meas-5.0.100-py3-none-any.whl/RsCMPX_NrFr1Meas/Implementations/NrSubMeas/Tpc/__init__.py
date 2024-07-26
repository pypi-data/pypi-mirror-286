from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TpcCls:
	"""Tpc commands group definition. 10 total commands, 3 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tpc", core, parent)

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def trace(self):
		"""trace commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_trace'):
			from .Trace import TraceCls
			self._trace = TraceCls(self._core, self._cmd_group)
		return self._trace

	@property
	def psteps(self):
		"""psteps commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_psteps'):
			from .Psteps import PstepsCls
			self._psteps = PstepsCls(self._core, self._cmd_group)
		return self._psteps

	def initiate(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: INITiate:NRSub:MEASurement<Instance>:TPC \n
		Snippet: driver.nrSubMeas.tpc.initiate() \n
		No command help available \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'INITiate:NRSub:MEASurement<Instance>:TPC', opc_timeout_ms)

	def stop(self) -> None:
		"""SCPI: STOP:NRSub:MEASurement<Instance>:TPC \n
		Snippet: driver.nrSubMeas.tpc.stop() \n
		No command help available \n
		"""
		self._core.io.write(f'STOP:NRSub:MEASurement<Instance>:TPC')

	def stop_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: STOP:NRSub:MEASurement<Instance>:TPC \n
		Snippet: driver.nrSubMeas.tpc.stop_with_opc() \n
		No command help available \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCMPX_NrFr1Meas.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'STOP:NRSub:MEASurement<Instance>:TPC', opc_timeout_ms)

	def abort(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: ABORt:NRSub:MEASurement<Instance>:TPC \n
		Snippet: driver.nrSubMeas.tpc.abort() \n
		No command help available \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'ABORt:NRSub:MEASurement<Instance>:TPC', opc_timeout_ms)

	def clone(self) -> 'TpcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TpcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
