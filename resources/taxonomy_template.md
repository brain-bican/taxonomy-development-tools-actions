## {{cas.title}}

{{cas.description}}

---

**Matrix File ID:** {{cas.matrix_file_id}}

**Cell Annotation URL:** {{cas.cellannotation_url}}

**Author name:** {{cas.author_name}}

**Author contact:** {{cas.author_contact}}

**Author orcid:** {{cas.orcid}}

{% if 'author_list' in cas %}
**Author list:** {{cas.author_list}}
{% endif %}

---

**Cell Annotation Schema Version:** {{cas.cellannotation_schema_version}}

**Cell Annotation Timestamp:** {{cas.cellannotation_timestamp}}

**Cell Annotation Version:** {{cas.cellannotation_version}}

---

**Labelsets:**

| Name | Description | Annotation Method | Rank |
|------|-------------|-------------------|------|
{% for labelset in cas.labelsets %}
|{{labelset.name}}|{{labelset.description}}|{{labelset.annotation_method}}|{{labelset.rank}}|
{% endfor %}