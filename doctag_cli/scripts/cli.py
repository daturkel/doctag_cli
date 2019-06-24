import os

import click
from doctag import TagIndex
from doctag_cli.utils import doc_str, get_ti, get_ti_file, initialize, tag_str


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    if ctx.invoked_subcommand is None:
        shell()
    else:
        pass


@cli.command()
def init():
    """Create a tag index at ~/.dtdb.json (or $DTDB if it is set).
    """
    try:
        ti = get_ti()
        print(f"Tag index already exists at {ti.loc}")
    except FileNotFoundError:
        tif = get_ti_file()
        ti = initialize(location=tif)
        print(f"Tag index initialized at {tif}.")


@cli.command()
def shell():
    click.echo("Shell!")


@cli.command()
@click.option(
    "-v", "--verbose", "verbose", is_flag=True, help="Show tags after each doc."
)
@click.argument("query", nargs=-1)
def find(query, verbose):
    """Find docs with a boolean tag QUERY.

    > dt find school or (book and class)
    """
    query = " ".join(query)
    ti = get_ti()
    results = ti.query(query=query)
    for doc in sorted(results):
        if not verbose:
            click.echo(doc)
        else:
            click.echo(f"{doc} ({tag_str(ti=ti,doc=doc)})")


@cli.command()
@click.argument("doc", nargs=1)
@click.argument("tags", nargs=-1)
def tag(doc, tags):
    """Apply TAGS to DOC. Tags are space-separated.

    > dt tag todo.txt list gtd

    See also `dt gat --help`.
    """
    with get_ti() as ti:
        ti.tag(docs=doc, tags=tags)


@cli.command()
@click.argument("tag", nargs=1)
@click.argument("docs", nargs=-1)
def gat(tag, docs):
    """Apply TAG to DOCS. Docs are space-separated.

    > dt gat list todo.txt movies.txt

    See also `dt tag --help`.
    """
    with get_ti() as ti:
        ti.tag(docs=docs, tags=tag)


@cli.command()
@click.argument("doc", nargs=1)
@click.argument("tags", nargs=-1)
def untag(doc, tags):
    """Remove TAGS from DOC. Tags are space-separated.

    > dt untag old_list.txt current important

    See also `dt ungat --help`.
    """
    with get_ti() as ti:
        ti.untag(docs=doc, tags=tags)


@cli.command()
@click.argument("tag", nargs=1)
@click.argument("docs", nargs=-1)
def ungat(tag, docs):
    """Remove TAG from DOCS. Docs are space-separated.

    > dt ungat current old_list.txt old_notes.txt

    See also `dt untag --help`.
    """
    with get_ti() as ti:
        ti.untag(docs=docs, tags=tag)


## begin `show` command group
@cli.group()
@click.pass_context
@click.option("-v", "--verbose", "verbose", is_flag=True, help="Show detailed output.")
def show(ctx, verbose):
    """Print either docs or tags to stdout.

    > dt show tags

    > dt show docs
    """
    ctx.obj["ti"] = get_ti()
    ctx.obj["verbose"] = verbose


@show.command()
@click.pass_obj
@click.option(
    "-v", "--verbose", "verbose", is_flag=True, help="Show tags after each doc."
)
def docs(obj, verbose):
    """Show all docs currently tagged.
    """
    ti = obj["ti"]
    verbose = obj["verbose"] or verbose
    doc_n = sorted(
        [(doc, len(ti.doc_to_tags[doc])) for doc in ti.docs],
        key=lambda x: (-x[1], x[0]),
    )
    for doc in doc_n:
        if not verbose:
            click.echo(message=f"{doc[0]} ({doc[1]})")
        else:
            click.echo(message=f"{doc[0]} ({tag_str(ti=ti,doc=doc[0])})")


@show.command()
@click.pass_obj
@click.option(
    "-v", "--verbose", "verbose", is_flag=True, help="Show docs after each tag."
)
def tags(obj, verbose):
    """Show all tags currently used.
    """
    ti = obj["ti"]
    verbose = obj["verbose"] or verbose
    tag_n = sorted(
        [(tag, len(ti.tag_to_docs[tag])) for tag in ti.tags],
        key=lambda x: (-x[1], x[0]),
    )
    for tag in tag_n:
        if not verbose:
            click.echo(message=f"{tag[0]} ({tag[1]})")
        else:
            click.echo(message=f"{tag[0]} ({doc_str(ti=ti,tag=tag[0])})")


## end "show" command group
## begin "remove" command group
@cli.group()
def remove():
    """Remove a doc or tag from the tag index.

    > dt remove tag old_tag

    > dt remove doc old_doc.txt
    """
    pass


@remove.command()
@click.argument("doc")
def doc(doc: str):
    """Remove DOC from the tag index. (i.e. remove all tags from DOC.)

    > dt remove doc old_file.txt
    """
    with get_ti() as ti:
        try:
            ti.remove_doc(doc_name=doc)
        except ValueError:
            click.echo(f"Doc '{doc}' not in index.")


@remove.command()
@click.argument("tag")
def tag(tag: str):
    """Remove TAG from the tag index. (i.e. remove TAG from all docs.)

    > dt remove tag old_tag
    """
    with get_ti() as ti:
        try:
            ti.remove_tag(tag=tag)
        except ValueError:
            click.echo(f"Tag '{tag}' not in index.")


@cli.command()
@click.argument("old_tags", nargs=-1)
@click.argument("new_tag", nargs=1)
def merge(old_tags, new_tag):
    """Merge OLD_TAGS into NEW_TAG. Old tags are space separated. New tag is created if it does not exist.

    > dt merge dairy diary

    (merges "dairy" into "diary")
    
    > dt merge lists lits list

    (merges "lists" and "lits" into "list")
    """
    with get_ti() as ti:
        ti.merge_tags(old_tags=old_tags, new_tag=new_tag)
