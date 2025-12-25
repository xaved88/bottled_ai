"""Tests for grid select handler - handles multi-card selection screens like Augmenter."""

import pytest
from unittest.mock import MagicMock

from rs.common.handlers.common_grid_select_handler import CommonGridSelectHandler


def create_mock_state(choices, num_cards=2, selected_count=0, for_transform=False):
    """Create a mock game state for GRID screen."""
    state = MagicMock()
    state.has_command.return_value = True
    state.get_choice_list.return_value = choices
    
    selected_cards = [{"name": "card"}] * selected_count
    
    state.game_state.return_value = {
        "screen_type": "GRID",
        "screen_state": {
            "for_transform": for_transform,
            "num_cards": num_cards,
            "selected_cards": selected_cards,
        }
    }
    return state


class TestGridSelectHandler:
    """Test grid select handler for Augmenter-style events."""

    def test_can_handle_grid_with_num_cards(self):
        """Handler should handle GRID screens with num_cards > 0."""
        handler = CommonGridSelectHandler(preferences=["strike"])
        state = create_mock_state(choices=["strike", "bash"], num_cards=2)
        assert handler.can_handle(state) == True

    def test_cannot_handle_zero_num_cards(self):
        """Handler should NOT handle GRID screens with num_cards=0."""
        handler = CommonGridSelectHandler(preferences=["strike"])
        state = create_mock_state(choices=["strike", "bash"], num_cards=0)
        assert handler.can_handle(state) == False

    def test_selects_correct_number_of_cards(self):
        """Should select num_cards cards."""
        handler = CommonGridSelectHandler(preferences=["strike"])
        state = create_mock_state(
            choices=["bash", "strike", "defend", "cleave"],
            num_cards=2,
            selected_count=0
        )
        
        action = handler.handle(state)
        choose_commands = [c for c in action.commands if c.startswith("choose")]
        assert len(choose_commands) == 2

    def test_accounts_for_already_selected(self):
        """Should only select remaining cards needed."""
        handler = CommonGridSelectHandler(preferences=["strike"])
        state = create_mock_state(
            choices=["bash", "strike", "defend"],
            num_cards=2,
            selected_count=1
        )
        
        action = handler.handle(state)
        choose_commands = [c for c in action.commands if c.startswith("choose")]
        assert len(choose_commands) == 1

    def test_confirms_when_all_selected(self):
        """Should just confirm when all cards already selected."""
        handler = CommonGridSelectHandler(preferences=["strike"])
        state = create_mock_state(
            choices=["bash", "strike"],
            num_cards=2,
            selected_count=2
        )
        
        action = handler.handle(state)
        choose_commands = [c for c in action.commands if c.startswith("choose")]
        assert len(choose_commands) == 0
        assert "confirm" in action.commands

    def test_ends_with_confirm(self):
        """All selections should end with confirm."""
        handler = CommonGridSelectHandler(preferences=["strike"])
        state = create_mock_state(choices=["bash", "strike"], num_cards=1)
        
        action = handler.handle(state)
        assert "confirm" in action.commands
