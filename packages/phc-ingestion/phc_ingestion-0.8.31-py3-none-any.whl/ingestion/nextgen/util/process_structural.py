from logging import Logger
import re
from typing import TypedDict

from ingestion.shared_util.coords_to_genes import coords_to_genes
from ingestion.nextgen.util.alteration_table import extract_variant_table
from ingestion.nextgen.util.interpretation import map_interpretation
from ingestion.nextgen.util.nextgen_specific_genes import (
    maybe_get_matching_gene_for_location,
    nextgen_specific_genes,
)
from ingestion.shared_util.open_maybe_gzipped import open_maybe_gzipped


class StructuralVariant(TypedDict):
    sample_id: str
    gene1: str
    gene2: str
    effect: str
    position1: tuple[str, str, str]
    position2: tuple[str, str, str]
    interpretation: str
    sequence_type: str
    in_frame: str
    attributes: dict


def structural_variant_to_csv_row(structural_variant: StructuralVariant) -> str:
    csv_row = ""
    for value in structural_variant.values():
        if isinstance(value, tuple):
            csv_row += ",".join(value)
        else:
            csv_row += f"{value}"
        csv_row += ","
    return f"{csv_row[:-1]}\n"


def are_variants_duplicates(sv1: StructuralVariant, sv2: StructuralVariant) -> bool:
    return (sv1["position1"] == sv2["position1"] and sv1["position2"] == sv2["position2"]) or (
        sv1["position1"] == sv2["position2"] and sv1["position2"] == sv2["position1"]
    )


def is_del_dup_or_ins(variant: list[str]) -> bool:
    return any([x in variant[2] for x in ["MantaDEL", "MantaDUP", "MantaINS"]])


def get_gene_from_coords(
    chromosome: str, start_position: str, end_position: str, log: Logger
) -> str:
    """
    A number of genes of interest with specific start and end positions have been provided.
    If a variant falls within the start and end positions of one of those genes of interest, that gene will be used.
    Otherwise, we fall back to the standard gene lookup.
    """
    center_position = int((int(start_position) + int(end_position)) / 2)

    gene = maybe_get_matching_gene_for_location(chromosome, center_position)
    if gene:
        return gene

    return coords_to_genes("GRCh38", chromosome, center_position, log)


def process_structural(
    sv_in_file: str, xml_in_file, root_path: str, prefix: str, log: Logger
) -> tuple[str | None, list[str]]:
    structural_variant_table = extract_variant_table(
        xml_in_file=xml_in_file, variant_type="structural", log=log
    )

    structural_variant_path_name = f"{root_path}/{prefix}.structural.csv"
    sample_id = prefix

    with open_maybe_gzipped(sv_in_file, "rt") as f:
        variants = [line for line in f.readlines() if not line.startswith("#")]

    structural_variants: list[StructuralVariant] = []
    for variant in variants:
        working_variant = variant.strip().split("\t")

        chromosome1 = f"chr{working_variant[0]}"
        start_position1 = working_variant[1]

        if is_del_dup_or_ins(working_variant):
            end_position1 = working_variant[7].split(";")[0].split("=")[1]
            chromosome2 = chromosome1
            start_position2 = start_position1
            end_position2 = end_position1
            effect = "duplication"
            if "MantaDEL" in working_variant[2]:
                effect = "deletion"
            elif "MantaINS" in working_variant[2]:
                effect = "insertion"

            # Get genes from coordinates using center point of start and end positions
            gene1 = get_gene_from_coords(chromosome1, start_position1, end_position1, log)
            gene2 = "N/A"

        else:
            alt = working_variant[4].strip("][TCGA").split(":")

            end_position1 = start_position1
            chromosome2 = f"chr{alt[0]}"
            start_position2 = alt[1]
            end_position2 = alt[1]
            effect = "translocation"

            # Get genes from coordinates using center point of start and end positions
            gene1 = get_gene_from_coords(chromosome1, start_position1, end_position1, log)
            gene2 = get_gene_from_coords(chromosome2, start_position2, end_position2, log)

        # Scrape interpretation
        interpretation = "unknown"
        if not structural_variant_table.empty:
            for _, row in structural_variant_table.iterrows():
                pattern = r"^.*\(.*(chr\d+:\d+).*;.*(chr\d+:\d+).*\).*$"
                match = re.match(pattern, row["gene"])
                if not match:
                    log.warn(f"Failed to parse gene field for structural variant")
                    continue
                ref_coords = set(match.groups())
                variant_coords = set(
                    [f"{chromosome1}:{start_position1}", f"{chromosome2}:{start_position2}"]
                )

                if ref_coords == variant_coords:
                    interpretation = map_interpretation(row["info"], log)

        # Hard-code
        sequence_type = "Somatic"
        in_frame = "Unknown"
        attributes: dict = {}

        structural_variants.append(
            {
                "sample_id": sample_id,
                "gene1": gene1,
                "gene2": gene2,
                "effect": effect,
                "position1": (chromosome1, start_position1, end_position1),
                "position2": (chromosome2, start_position2, end_position2),
                "interpretation": interpretation,
                "sequence_type": sequence_type,
                "in_frame": in_frame,
                "attributes": attributes,
            }
        )

    # Dedupe structural variants based on chromosome and positions
    deduped_structural_variants: list[StructuralVariant] = []
    for sv in structural_variants:
        maybe_matching_variant = next(
            (
                variant
                for variant in deduped_structural_variants
                if are_variants_duplicates(sv, variant)
            ),
            None,
        )
        if not maybe_matching_variant:
            deduped_structural_variants.append(sv)

    if not deduped_structural_variants:
        log.info(f"Ignoring empty structural variant file {sv_in_file}")
        return (None, [])

    log.info(f"Saving file to {structural_variant_path_name}")
    with open(structural_variant_path_name, "w+") as f:
        f.write(
            "sample_id,gene1,gene2,effect,chromosome1,start_position1,end_position1,chromosome2,start_position2,end_position2,interpretation,sequence_type,in-frame,attributes\n"
        )
        for sv in deduped_structural_variants:
            f.write(structural_variant_to_csv_row(sv))

    log.info("Finding structural variant translocations for genes of interest")
    translocations = [sv for sv in deduped_structural_variants if sv["effect"] == "translocation"]
    formatted_translocations: set[str] = set()
    for translocation in translocations:
        gene1, gene2 = translocation["gene1"], translocation["gene2"]
        # MYC is a special case
        if gene1 == "MYC" or gene2 == "MYC":
            if gene1 == gene2:
                continue
            formatted_translocations.add("t(MYC)")
            continue
        if gene1 in nextgen_specific_genes and gene2 in nextgen_specific_genes:
            chr1, chr2 = int(translocation["position1"][0][3:]), int(
                translocation["position2"][0][3:]
            )
            if chr1 == chr2:
                continue
            # Ensure chromosomes are in ascending order
            if chr1 > chr2:
                chr1, chr2 = chr2, chr1
            formatted_translocations.add(f"t({chr1};{chr2})")

    log.info(f"Found {len(formatted_translocations)} translocations for genes of interest")

    return structural_variant_path_name, list(formatted_translocations)
