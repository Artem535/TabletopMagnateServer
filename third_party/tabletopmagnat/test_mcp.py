from typing import Literal, Optional, Annotated
import yaml
from fastmcp import FastMCP
from pydantic import Field

from objectbox import (
    Box,
    Entity,
    Float32Vector,
    HnswIndex,
    Id,
    Store,
    String,
    VectorDistanceType,
    Int16,
)
from sentence_transformers import SentenceTransformer


# ------------------------------------------------------------------
# ObjectBox entities
# ------------------------------------------------------------------
@Entity()
class Rule:
    id = Id
    internal_id = String
    content = String
    section = String
    game = String
    req_term = String
    scenario = String
    priority = Int16
    zone = String
    vector = Float32Vector(index=HnswIndex(dimensions=768))


@Entity()
class Terminology:
    id = Id
    internal_id = String
    content = String
    name = String
    slug = String
    kind = String
    path = String
    group = String
    definition = String
    extra = String
    vector = Float32Vector(index=HnswIndex(dimensions=768))


# ------------------------------------------------------------------
# Global setup
# ------------------------------------------------------------------
COUNT_ITEMS = 3
server = FastMCP(name="rules-mcp")
store = Store(directory="./db")
rules_box = Box(store, entity=Rule)
terminology_box = Box(store, entity=Terminology)
model = SentenceTransformer("./model")


# ------------------------------------------------------------------
# Tools – parameters described inline with Annotated[…, Field(…)]
# ------------------------------------------------------------------
@server.tool
def find_in_rulebook(
    game_name: Annotated[str, Field(...)],
    section: Annotated[str, Field(...)],
    type_: Annotated[str, Field(...)],
    query: Annotated[str, Field(...)],
    # zone: Annotated[Literal["base", "advanced", "edge"], Field(...)] = "base",
) -> str:
    """
    Search for rules in the rulebook using vector similarity.

    Parameters
    ----------
    game_name : str
        Name of the game (required).
    section : str
        Section of the rulebook;.
    type_ : str
        Entity type to search (rule/action/setup/components/etc).
    query : str
        Natural-language search query (can be empty).
    zone : {'base','advanced','edge'}
        Rule zone; defaults to 'base'.
    """
    search_query = f"#game:{game_name} #section:{section} #type:{type_}\n---\n{query}"
    vector = model.encode(search_query)

    obx_query = rules_box.query(
        Rule.vector.nearest_neighbor(vector, element_count=COUNT_ITEMS)
        # & Rule.zone.equals(zone)
    ).build()

    results = []
    for id_, score in obx_query.find_ids_with_scores():
        r = rules_box.get(id_)
        results.append(
            {
                "id": r.id,
                "internal_id": r.internal_id,
                "content": r.content,
                "score": score,
                "game": r.game,
                "section": r.section,
                "req_term": yaml.safe_load(r.req_term),
                "scenario": r.scenario,
                "priority": r.priority,
                "zone": r.zone,
            }
        )

    return yaml.safe_dump(results, allow_unicode=True)


@server.tool
def find_in_terminology(
    game_name: Annotated[str, Field(...)],
    group: Annotated[str, Field(...)] = "default",
    query: Annotated[str, Field(...)] = "",
) -> str:
    """
    Search for terminology entries (kind=TERM) using vector similarity.

    Parameters
    ----------
    game_name : str
        Name of the game (required).
    group : str
        Terminology group; defaults to 'default'.
    query : str
        Text query for semantic term search.
    """
    search_query = f"#game:{game_name} #group:{group}\n---\n{query}"
    vector = model.encode(search_query)

    obx_query = terminology_box.query(
        Terminology.vector.nearest_neighbor(vector, element_count=COUNT_ITEMS)
        & Terminology.kind.equals("TERM")
    ).build()

    results = []
    for id_, score in obx_query.find_ids_with_scores():
        t = terminology_box.get(id_)
        results.append(
            {
                "id": t.internal_id,
                "score": score,
                "content": t.content,
                "name": t.name,
                "group": t.group,
                "definition": t.definition,
                "extra": yaml.safe_load(t.extra),
                "kind": t.kind,
            }
        )

    return yaml.safe_dump(results, allow_unicode=True)


@server.tool
def find_in_terminology_ner(
    game_name: Annotated[str, Field(...)],
    group: Annotated[str, Field(...)] = "default",
    query: Annotated[str, Field(...)] = "",
) -> str:
    """
    Search for entity-level terminology (kind=ENTITY) using vector similarity.

    Parameters
    ----------
    game_name : str
        Name of the game (required).
    group : str
        Terminology group; defaults to 'default'.
    query : str
        Text query for semantic term search.
    """
    search_query = f"#game:{game_name} #group:{group}\n---\n{query}"
    vector = model.encode(search_query)

    obx_query = terminology_box.query(
        Terminology.vector.nearest_neighbor(vector, element_count=COUNT_ITEMS)
        & Terminology.kind.equals("ENTITY")
    ).build()

    results = []
    for id_, score in obx_query.find_ids_with_scores():
        t = terminology_box.get(id_)
        results.append(
            {
                "id": t.internal_id,
                "score": score,
                "content": t.content,
                "name": t.name,
                "group": t.group,
                "definition": t.definition,
                "extra": yaml.safe_load(t.extra),
                "kind": t.kind,
            }
        )

    return yaml.safe_dump(results, allow_unicode=True)


# ------------------------------------------------------------------
# Run the MCP server
# ------------------------------------------------------------------
if __name__ == "__main__":
    server.run("http", port=8000)
