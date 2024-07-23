from logging import Logger

from ingestion.shared_util.open_maybe_gzipped import open_maybe_gzipped


def build_variant_key_from_vcf_line(line: str) -> str:
    split_line = line.strip().split("\t")
    chrom, pos, ref, alt = split_line[0], split_line[1], split_line[3], split_line[4]
    return f"{chrom}:{pos}:{ref}:{alt}"


def extract_filter_from_vcf_line(line: str) -> str:
    split_line = line.strip().split("\t")
    return split_line[6]


def replace_filter_in_vcf_line(line: str, new_filter: str) -> str:
    split_line = line.strip().split("\t")
    split_line[6] = new_filter
    return "\t".join(split_line) + "\n"


def pre_filter_somatic_vcf(
    somatic_vcf_file: str,
    somatic_vcf_snv_file: str,
    somatic_vcf_indel_file: str,
    working_dir: str,
    log: Logger,
) -> str:
    """
    Removes all variants from the `somatic_vcf_file` that are not
    also in the `somatic_vcf_snv_file` or `somatic_vcf_indel_file`.

    Also updates the FILTER field in the `somatic_vcf_file` to match
    the FILTER field of the corresponding variant in the
    `somatic_vcf_snv_file` or `somatic_vcf_indel_file`.
    """
    log.info("Pre-filtering somatic VCF file")

    valid_variants_with_filters: dict[str, str] = {}

    for file in [somatic_vcf_snv_file, somatic_vcf_indel_file]:
        with open_maybe_gzipped(file, "rt") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                valid_variants_with_filters[build_variant_key_from_vcf_line(line)] = (
                    extract_filter_from_vcf_line(line)
                )

    log.info(f"Found {len(valid_variants_with_filters)} valid variants")

    output_vcf_path = f"{working_dir}/filtered_somatic.vcf.gz"
    with (
        open_maybe_gzipped(somatic_vcf_file, "rt") as f,
        open_maybe_gzipped(output_vcf_path, "wt") as w,
    ):
        for line in f:
            if line.startswith("#"):
                w.write(line)
            else:
                key = build_variant_key_from_vcf_line(line)
                if key in valid_variants_with_filters:
                    w.write(replace_filter_in_vcf_line(line, valid_variants_with_filters[key]))

    log.info(f"Successfully pre-filtered somatic VCF file to {output_vcf_path}")
    return output_vcf_path
