# Geneyx Analysis API Postman Collection

This collection provides programmatic access to **Geneyx Analysis**, enabling integration with external systems such as LIMS, EHRs, and internal pipelines. It supports a wide range of functions including sample and case management, annotation workflows, metadata retrieval, and file handling.

---

## 🔐 Authentication

To authenticate requests:

1. Open the **Postman Collection Settings**
2. Go to the **Variables** tab
3. Set the following variables:
   - `ApiUserId`
   - `ApiUserKey`
   - `CustomerAccountKey` (if applicable)

These credentials will automatically populate the headers of all API calls.

---

## 🌍 Supported Server URLs

Update the `baseURL` variable based on your deployment:

- **Global Server**: `https://analysis.geneyx.com/`
- **US Server**: `https://ga-us.geneyx.com/`
- **China Server**: `https://fa.shanyint.com/`


---

## 📥 Importing the Collection into Postman

1. Download [Postman](https://www.postman.com/downloads/)
2. Open the app and click **Import**
3. Upload `collection.json`

Once imported, navigate to the collection, set your variables, and begin testing endpoints.

---

## 🧪 Best Practices

- Use the `Page` and `PageSize` parameters when retrieving lists to manage pagination
- Use exact names/IDs for fields like `SampleSn`, `PatientId`, `ProtocolId`, etc.
- A response with `"Data": true` typically indicates a successfully initiated operation (e.g., annotation or deletion)
- Check `Info` and `MoreInfo` fields in responses for additional debug information when needed

---

## 🆘 Need Help?

If you require access credentials or technical assistance, contact:

📧 **support@geneyx.com**

---

