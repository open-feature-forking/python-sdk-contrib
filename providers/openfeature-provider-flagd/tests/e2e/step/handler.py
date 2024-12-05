import logging
import time

import pytest
from pytest_bdd import given, parsers, then, when

from openfeature.client import OpenFeatureClient
from openfeature.event import ProviderEvent


@pytest.fixture()
def event_handles() -> list:
    return []


@given(
    parsers.cfparse(
        "a {event_type:ProviderEvent} handler was added",
        extra_types={"ProviderEvent": ProviderEvent},
    ),
)
def add_event_handler(
    client: OpenFeatureClient, event_type: ProviderEvent, event_handles: list
):
    def handler(event):
        logging.debug((event_type, event))
        event_handles.append(
            {
                "type": event_type,
                "event": event,
            }
        )

    client.add_handler(event_type, handler)


def assert_handlers(
    handles, event_type: ProviderEvent, max_wait: int = 2, num_events: int = 1
):
    # we want to listen to all the events from now on
    poll_interval = 1
    while max_wait > 0:
        if sum([h["type"] == event_type for h in handles]) < num_events:
            max_wait -= poll_interval
            time.sleep(poll_interval)
            continue
        break

    logging.info(f"asserting num({event_type}) >= {num_events}: {handles}")
    actual_num_events = sum([h["type"] == event_type for h in handles])
    assert (
        num_events <= actual_num_events
    ), f"Expected {num_events} but got {actual_num_events}: {handles}"


@when(
    parsers.cfparse(
        "a {event_type:ProviderEvent} was fired",
        extra_types={"ProviderEvent": ProviderEvent},
    )
)
def event_handler_trigger_event(event_type: ProviderEvent, event_handles: list):
    pass


@then(
    parsers.cfparse(
        "the {event_type:ProviderEvent} handler must run",
        extra_types={"ProviderEvent": ProviderEvent},
    )
)
def assert_handler_run(event_type: ProviderEvent, event_handles):
    assert_handlers(event_handles, event_type, max_wait=30)

    for event in event_handles:
        if event["type"] == event_type:
            event_handles.remove(event)
