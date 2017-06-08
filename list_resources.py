import visa

rm = visa.ResourceManager();
print(rm.list_resources());
